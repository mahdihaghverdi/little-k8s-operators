# Hello Operator

A beginner-friendly Kubernetes Operator built with **Knopf** to demonstrate the fundamentals of Kubernetes Operator development.

This project is the first repository in my Kubernetes Operator learning series. The goal is to understand how Operators work internally by building them from scratch, starting with the simplest possible example and gradually moving toward production-grade Operators.

---
## Problem Statement

Imagine multiple teams need `ConfigMap`s with different messages.

Without an Operator, every `ConfigMap` must be created, updated, and maintained manually. If someone accidentally deletes or modifies it, Kubernetes won't restore the expected configuration automatically.

The Hello Operator automates this workflow by continuously reconciling the desired state.

---

## Custom Resource Example

```yaml
apiVersion: demo.demo.io/v1
kind: Hello
metadata:
  name: backend
spec:
  message: Hello Backend
```

---

## Generated Resource

The operator creates the following ConfigMap automatically:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend
data:
  message: Hello Backend
```

---

## Features

- Create a `ConfigMap` from a custom resource
- Keep the `ConfigMap` synchronized with the CR specification
- Automatically recreate deleted `ConfigMap`s (self-healing)
- Delete owned resources when the CR is deleted
- Update resource status after successful reconciliation
- Fully idempotent reconciliation logic
