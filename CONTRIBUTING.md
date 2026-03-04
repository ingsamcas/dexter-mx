# Contributing to Dexter MX

Gracias por tu interés en contribuir a Dexter MX. Este documento proporciona guías para hacer contribuciones efectivas.

## 📋 Reportar Issues

Si encuentras un bug o tienes una sugerencia:

1. **Busca primero**: Revisa si ya existe un issue similar
2. **Usa el template**: Proporciona información detallada
3. **Incluye**:
   - Sistema operativo
   - Versión de Python
   - Mensajes de error completos
   - Pasos para reproducir el problema

## 🔧 Pull Requests

### Antes de empezar

1. Fork el repositorio
2. Clona tu fork localmente
3. Crea una rama con nombre descriptivo:
   ```bash
   git checkout -b feat/amazing-feature
   # o
   git checkout -b fix/critical-bug
   ```

### Nomenclatura de branches

- `feat/` - Nuevas funcionalidades
- `fix/` - Correcciones de bugs
- `docs/` - Cambios en documentación
- `refactor/` - Refactorización de código
- `test/` - Agregar o modificar tests

### Formato de commits

Usa [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): descripción corta

Descripción más detallada si es necesario.

Fixes #123
```

**Tipos**:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formato, punto y coma, etc.
- `refactor`: Refactorización
- `test`: Agregar tests
- `chore`: Actualizar dependencias, etc.

**Ejemplos**:
```bash
feat(databursatil): add support for options data
fix(agent): prevent infinite loop in FIBRA analysis
docs(readme): update installation instructions
```

### Guías de código

1. **Python Style**:
   - Sigue [PEP 8](https://pep8.org/)
   - Usa type hints cuando sea posible
   - Máximo 100 caracteres por línea

2. **Docstrings**:
   ```python
   def function_name(param: str) -> dict:
       """
       Brief description.
       
       Args:
           param: Description of parameter
       
       Returns:
           Description of return value
       """
   ```

3. **Testing**:
   - Agrega tests para nuevas funcionalidades
   - Asegúrate que todos los tests pasen:
     ```bash
     uv run pytest
     ```

4. **Documentación**:
   - Actualiza README.md si agregas features
   - Actualiza CHANGELOG.md con tus cambios
   - Agrega docstrings a funciones nuevas

### Proceso de PR

1. **Push a tu branch**:
   ```bash
   git push origin feat/amazing-feature
   ```

2. **Abre un Pull Request** en GitHub

3. **Descripción del PR**:
   - Resumen claro de los cambios
   - Referencia a issues relacionados
   - Screenshots si hay cambios visuales

4. **Template de PR**:
   ```markdown
   ## Descripción
   [Descripción clara de los cambios]
   
   ## Tipo de cambio
   - [ ] Bug fix
   - [ ] Nueva funcionalidad
   - [ ] Breaking change
   - [ ] Documentación
   
   ## Testing
   - [ ] Tests agregados/actualizados
   - [ ] Todos los tests pasan
   
   ## Checklist
   - [ ] Código sigue las guías de estilo
   - [ ] Documentación actualizada
   - [ ] CHANGELOG.md actualizado
   ```

## 🧪 Testing local

Antes de hacer push:

```bash
# Instalar dependencias
uv sync

# Verificar sintaxis
uv run python -m py_compile src/dexter/**/*.py

# Correr tests
uv run pytest

# Test con Docker
docker build -t dexter-mx .
./dexter.sh compare
```

## 🌐 Áreas de contribución

### Prioritarias

1. **Nuevas fuentes de datos**: Lápiz, Alpha Vantage, etc.
2. **Mejoras de DataBursatil**: Más endpoints, mejor manejo de errores
3. **Tests**: Aumentar cobertura de tests
4. **Documentación**: Tutoriales, guías de uso

### Bienvenidas

- Optimizaciones de performance
- Mejoras de UX en CLI
- Soporte para más mercados (Colombia, Chile, etc.)
- Integración con más LLM providers

### No prioritarias (pero aceptadas)

- Migraciones de lenguaje (ej. Kotlin)
- Features muy específicas
- Cambios cosméticos sin valor funcional

## ❓ Preguntas

Si tienes dudas:

1. Abre un [Discussion](https://github.com/ingsamcas/dexter-mx/discussions)
2. Revisa issues existentes
3. Contacta al maintainer

## 🎉 Reconocimiento

Los contributors serán reconocidos en:
- README.md (sección Contributors)
- Releases notes
- Commits con Co-authored-by

## 📜 Código de Conducta

- Sé respetuoso y profesional
- Acepta feedback constructivo
- Enfócate en la calidad sobre la cantidad
- Ayuda a otros contributors

---

¡Gracias por contribuir a Dexter MX! 🚀
