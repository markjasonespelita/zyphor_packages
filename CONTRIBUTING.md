# 📦 Zyphor Packages (zyphor_packages)

## 📌 Purpose
The `zyphor_packages` repository contains **execution-level tools and modules** used by Zyphor OS.

It provides:

- Internal CLI modules
- System automation scripts
- Install/uninstall logic
- Zyphor system tools

---

## 🧠 Modules

All modules must be placed under:

```
/modules/<module-name>/
```

Each module must include:

```
install.sh
remove.sh
```

---

## 🧩 Example Structure

```
modules/example-module/
  ├── install.sh
  ├── remove.sh
```

---

## ⚙️ Module Requirements

Every module must:

- Be reversible (install + uninstall)
- Clean up all installed files
- Avoid leaving system traces
- Work on Ubuntu/Debian systems

---

## 🧪 Testing

Before submitting:

```bash
bash install.sh
bash remove.sh
```

Ensure:

- No errors
- Clean install
- Clean removal
- No leftover files or services

---

## 🚫 Forbidden Contributions

Do NOT include:

- Malicious scripts
- Hidden background processes
- Remote execution without consent
- Destructive system commands
- Unverified binaries

---

## 🚀 Contribution Flow

1. Fork repository
2. Create or modify module
3. Test locally
4. Ensure clean uninstall
5. Submit Pull Request
6. Await review

---

## 💡 Philosophy

> This repo is the **execution layer of Zyphor OS**

It must always remain:

- clean
- reversible
- predictable
- safe

---

# 🧭 Final Note

If `zyphor_repo` is the brain,
then `zyphor_packages` is the muscles.