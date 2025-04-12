# Hello, I'm EQ.

Hi!  
I tried to make a program that compiles multiple programs into one, called **Binder**.  
I'm not very good at English — all of this is done using Google Translate.  
If you understand something or have questions, please [Email me](mailto:dexedusd@gmail.com)

## Workflow Diagram - EXE Binder

```mermaid
graph TD
    A[Start] --> B[User Inputs EXE File 1 and 2 or via args]
    B --> C[embed_files.py reads EXE files as bytes]
    C --> D[Generate embedded dict in loader.py]
    D --> E[loader.py writes EXEs to temp files]
    E --> F[Run EXEs with threading and subprocess]
    F --> G[main.py builds loader.py into one EXE with Nuitka]
    G --> H[Output: Single EXE for both programs]
    H --> I[Done]

    style A fill:#212121,stroke:#ffffff,stroke-width:2px
    style B fill:#424242,stroke:#ffffff,stroke-width:2px
    style C fill:#616161,stroke:#ffffff,stroke-width:2px
    style D fill:#757575,stroke:#ffffff,stroke-width:2px
    style E fill:#9E9E9E,stroke:#ffffff,stroke-width:2px
    style F fill:#BDBDBD,stroke:#ffffff,stroke-width:2px
    style G fill:#E0E0E0,stroke:#ffffff,stroke-width:2px
    style H fill:#EEEEEE,stroke:#ffffff,stroke-width:2px
    style I fill:#FFFFFF,stroke:#000000,stroke-width:2px

