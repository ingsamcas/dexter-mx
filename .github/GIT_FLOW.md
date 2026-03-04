# Git Flow para Dexter MX

## Estructura de Ramas

- **`main`**: Código de producción estable. Solo recibe merges desde `develop` via squash commits.
- **`develop`**: Rama de desarrollo activo. Todas las features y fixes se trabajan aquí.
- **`feature/*`**: Ramas de features específicas (opcional, para features grandes).
- **`hotfix/*`**: Fixes urgentes que se mergean directo a `main` y luego a `develop`.

## Workflow

### Desarrollo Normal

```bash
# Trabajar en develop
git checkout develop
git pull origin develop

# Hacer cambios
# ... editar archivos ...

# Commit
git add .
git commit -m "feat: descripción del cambio"
git push origin develop
```

### Merge a Main (Squash)

Cuando `develop` está listo para producción:

```bash
# Desde develop, asegurar que está actualizado
git checkout develop
git pull origin develop

# Cambiar a main
git checkout main
git pull origin main

# Squash merge desde develop
git merge --squash develop
git commit -m "release: descripción de los cambios acumulados

- Feature 1
- Feature 2
- Fix 3
"

git push origin main

# Regresar a develop para seguir trabajando
git checkout develop
```

### Hotfix Urgente

Para fixes que no pueden esperar al siguiente release:

```bash
# Crear rama desde main
git checkout main
git checkout -b hotfix/critical-bug

# Fix
# ... editar ...

# Commit
git commit -m "fix: critical bug description"

# Merge a main
git checkout main
git merge hotfix/critical-bug
git push origin main

# Merge a develop también
git checkout develop
git merge hotfix/critical-bug
git push origin develop

# Eliminar rama hotfix
git branch -d hotfix/critical-bug
```

## Reglas

1. **NUNCA** hacer commits directos a `main`
2. Todos los cambios van primero a `develop`
3. Merges a `main` SIEMPRE con `--squash` para mantener historial limpio
4. `main` debe estar siempre en estado "deployable"
5. Tags de versión solo en `main` (ej. `v1.0.0`, `v1.1.0`)

## Estado Actual

- Rama activa para desarrollo: **`develop`**
- Última versión en `main`: **v1.0.0** (Mexican market adaptation)
