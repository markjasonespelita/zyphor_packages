// zyshell - Zyphor OS Shell
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <termios.h>

#define BUFFER_SIZE 1024
#define MAX_ARGS    64
#define MAX_HISTORY 100

// ── History ──────────────────────────────────────────────────────────────────
static char  *history[MAX_HISTORY];
static int    history_len = 0;

void history_add(const char *line)
{
    // skip blank lines and duplicates at the top
    if (line[0] == '\0') return;
    if (history_len > 0 && strcmp(history[history_len - 1], line) == 0) return;

    if (history_len == MAX_HISTORY) {
        free(history[0]);
        memmove(history, history + 1, (MAX_HISTORY - 1) * sizeof(char *));
        history_len--;
    }
    history[history_len++] = strdup(line);
}

// ── Raw-mode helpers ──────────────────────────────────────────────────────────
static struct termios orig_termios;

void raw_enable(void)
{
    struct termios raw;
    tcgetattr(STDIN_FILENO, &orig_termios);
    raw = orig_termios;
    // disable canonical mode, echo, and signals
    raw.c_lflag &= ~(ICANON | ECHO | ISIG);
    raw.c_cc[VMIN]  = 1;
    raw.c_cc[VTIME] = 0;
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw);
}

void raw_disable(void)
{
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &orig_termios);
}

// Redraw the current input line (overwrites whatever was there).
void redraw_line(const char *prompt_str, const char *buf)
{
    // \r   = go to column 0
    // \033[K = erase to end of line
    printf("\r\033[K%s%s", prompt_str, buf);
    fflush(stdout);
}

// ── Prompt builder ────────────────────────────────────────────────────────────
// Returns a heap-allocated prompt string (caller must free).
char *build_prompt(void)
{
    char  hostname[256];
    char  cwd[1024];
    char *username;
    char *buf;

    username = getenv("USER");
    if (!username) username = "unknown";
    gethostname(hostname, sizeof(hostname));
    getcwd(cwd, sizeof(cwd));

    // worst case: ANSI codes + strings + "$ \0"
    size_t len = 64 + strlen(username) + strlen(hostname) + strlen(cwd);
    buf = malloc(len);
    snprintf(buf, len,
        "\033[1;35m%s\033[0m@\033[1;36m%s\033[0m:\033[1;34m%s\033[0m$ ",
        username, hostname, cwd);
    return buf;
}

void show_prompt(void)
{
    char *p = build_prompt();
    fputs(p, stdout);
    fflush(stdout);
    free(p);
}

// ── Line reader with arrow-key history ───────────────────────────────────────
// Fills `out` (size BUFFER_SIZE) with the entered line (no trailing newline).
// Returns 0 on success, -1 on EOF.
int read_line(char *out)
{
    char  buf[BUFFER_SIZE] = {0};
    int   len    = 0;
    int   cursor = 0;           // ← new: cursor position within buf
    int   hidx   = history_len;
    char  saved[BUFFER_SIZE] = {0};

    char *prompt = build_prompt();
    fputs(prompt, stdout);
    fflush(stdout);

    raw_enable();

    while (1) {
        unsigned char c;
        if (read(STDIN_FILENO, &c, 1) <= 0) {
            raw_disable();
            free(prompt);
            return -1;
        }

        if (c == '\r' || c == '\n') {
            putchar('\n');
            break;

        } else if (c == 127 || c == '\b') {
            // backspace: delete char before cursor
            if (cursor > 0) {
                memmove(&buf[cursor - 1], &buf[cursor], len - cursor);
                len--;
                cursor--;
                buf[len] = '\0';
                redraw_line(prompt, buf);
                // reposition cursor: move to end, then back
                if (len > cursor) {
                    printf("\033[%dD", len - cursor);
                    fflush(stdout);
                }
            }

        } else if (c == '\x1b') {
            unsigned char seq[2];
            if (read(STDIN_FILENO, &seq[0], 1) <= 0) continue;
            if (read(STDIN_FILENO, &seq[1], 1) <= 0) continue;
            if (seq[0] != '[') continue;

            if (seq[1] == 'A') {
                // ↑
                if (hidx == history_len)
                    strncpy(saved, buf, BUFFER_SIZE);
                if (hidx > 0) {
                    hidx--;
                    strncpy(buf, history[hidx], BUFFER_SIZE - 1);
                    len = cursor = strlen(buf);
                    redraw_line(prompt, buf);
                }

            } else if (seq[1] == 'B') {
                // ↓
                if (hidx < history_len) {
                    hidx++;
                    const char *src = (hidx == history_len) ? saved : history[hidx];
                    strncpy(buf, src, BUFFER_SIZE - 1);
                    len = cursor = strlen(buf);
                    redraw_line(prompt, buf);
                }

            } else if (seq[1] == 'C') {
                // →
                if (cursor < len) {
                    cursor++;
                    printf("\033[C");
                    fflush(stdout);
                }

            } else if (seq[1] == 'D') {
                // ←
                if (cursor > 0) {
                    cursor--;
                    printf("\033[D");
                    fflush(stdout);
                }
            }

        } else if (c >= 32 && c < 127) {
            if (len < BUFFER_SIZE - 1) {
                memmove(&buf[cursor + 1], &buf[cursor], len - cursor);
                buf[cursor++] = c;
                len++;              // ← only once
                buf[len] = '\0';
                redraw_line(prompt, buf);
                if (len > cursor) {
                    printf("\033[%dD", len - cursor);
                    fflush(stdout);
                }
            }
        }
    }

    raw_disable();
    free(prompt);
    strncpy(out, buf, BUFFER_SIZE);
    return 0;
}

// ── Command helpers ───────────────────────────────────────────────────────────
void parse_command(char *input, char *args[])
{
    int i = 0;
    args[i] = strtok(input, " \n");
    while (args[i] != NULL && i < MAX_ARGS - 1) {
        i++;
        args[i] = strtok(NULL, " \n");
    }
    args[i] = NULL;
}

// ── Zyphor Os Shell ──────────────────────────────────────────────────────────────────────

void show_os_screen(void)
{
    printf("\n");

    // Logo
    printf("\033[1;35m"
        " ______              _\n"
        "|___  /             | |\n"
        "   / / _   _  _ __  | |__    ___   _ __\n"
        "  / / | | | || '_ \\| '_ \\  / _ \\ | '__|\n"
        " / /__| |_| || |_) || | | || (_) || |\n"
        "/_____||__, || .__/ |_| |_| \\___/ |_|\n"
        "        __/ || |          Operating System\n"
        "       |___/ |_|\n"
        "\033[0m\n");

    // Parse /etc/os-release for PRETTY_NAME and VERSION_ID
    char pretty_name[256] = "Zyphor OS";
    char version_id[64]   = "unknown";

    FILE *f = fopen("/etc/os-release", "r");
    if (f) {
        char line[512];
        while (fgets(line, sizeof(line), f)) {
            // strip trailing newline
            line[strcspn(line, "\n")] = '\0';

            if (strncmp(line, "PRETTY_NAME=", 12) == 0) {
                char *val = line + 12;
                // strip surrounding quotes if present
                if (val[0] == '"') {
                    val++;
                    val[strcspn(val, "\"")] = '\0';
                }
                strncpy(pretty_name, val, sizeof(pretty_name) - 1);
            }

            if (strncmp(line, "VERSION_ID=", 11) == 0) {
                char *val = line + 11;
                if (val[0] == '"') {
                    val++;
                    val[strcspn(val, "\"")] = '\0';
                }
                strncpy(version_id, val, sizeof(version_id) - 1);
            }
        }
        fclose(f);
    }

    // OS info line
    printf("  \033[90mOS\033[0m      \033[35m%s\033[0m\n", pretty_name);
    printf("  \033[90mVERSION\033[0m \033[35m%s\033[0m\n", version_id);

    // Boot log
    printf("\033[32m[  OK  ]\033[0m \033[90mStarted zyshell (Zyphor OS Shell)\033[0m\n");

    printf("\n\033[90m────────────────────────────────────────\033[0m\n\n");
}

// ── Main ──────────────────────────────────────────────────────────────────────
int main(void)
{

    // Show shell banner
    show_os_screen();

    char  input[BUFFER_SIZE];
    char *args[MAX_ARGS];

    while (1) {
        if (read_line(input) < 0)
            break; // EOF

        if (input[0] == '\0')
            continue; // empty line

        history_add(input);

        // make a copy for strtok (it mutates the string)
        char tmp[BUFFER_SIZE];
        strncpy(tmp, input, BUFFER_SIZE);
        parse_command(tmp, args);

        if (args[0] == NULL)
            continue;

        if (strcmp(args[0], "exit") == 0)
            break;

        if (strcmp(args[0], "cd") == 0) {
            const char *dir = args[1];
            if (dir == NULL) {
                dir = getenv("HOME");
                if (dir == NULL) dir = "/";
            }
            if (chdir(dir) != 0)
                perror("zysh");
            continue;
        }

        if (strcmp(args[0], "ls") == 0) {
            char *colored_args[MAX_ARGS + 1];
            colored_args[0] = "ls";
            colored_args[1] = "--color=auto";
            int i;
            for (i = 1; args[i] != NULL && i < MAX_ARGS - 1; i++)
                colored_args[i + 1] = args[i];
            colored_args[i + 1] = NULL;

            pid_t pid = fork();
            if (pid == 0) {
                execvp("ls", colored_args);
                perror("zysh");
                _exit(1);
            } else if (pid > 0) {
                wait(NULL);
            } else {
                perror("fork");
            }
            continue;
        }

        pid_t pid = fork();
        if (pid == 0) {
            execvp(args[0], args);
            perror("zysh");
            _exit(1);
        } else if (pid > 0) {
            wait(NULL);
        } else {
            perror("fork");
        }
    }

    printf("Exiting zyshell...\n");
    return 0;
}