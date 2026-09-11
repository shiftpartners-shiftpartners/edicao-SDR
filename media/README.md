# Media workspace

Os arquivos de mídia não devem ser versionados por padrão.

Estrutura local recomendada:

```text
media/
├── source/          # originais imutáveis
├── work/            # intermediários locais
├── contact-sheets/  # inspeção visual
└── renders/         # saídas locais
```

Essas pastas estão protegidas pelo `.gitignore`.

## Regras

- manter `source/` imutável;
- nunca commitar material bruto, render pesado ou arquivo sensível sem necessidade explícita;
- usar nomes rastreáveis por conceito, hook, execução, formato e versão;
- guardar no Git apenas planos, metadados, templates, documentação e scripts necessários para reproduzir o trabalho;
- revisar direitos de uso antes de incorporar qualquer asset externo.
