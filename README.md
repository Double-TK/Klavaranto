## ES | Español

# Klavaranto v1.1.2

## Características

* Convierte combinaciones de teclas en caracteres especiales del Esperanto (cx→ĉ, gx→ĝ, hx→ĥ, jx→ĵ, sx→ŝ, ux→ŭ)
* Métodos de entrada configurables: prefijo, sufijo o doble tecla
* Sistema de deshacer — repitiendo el afijo o con una tecla personalizada
* Atajo de activación configurable, funciona aunque queden teclas modificadoras "pegadas"
* Interfaz multi-idioma: Español, English, Esperanto
* Opción para iniciar el programa ya activado
* Opción para iniciar junto con Windows
* Ícono en la bandeja del sistema con menú rápido

## Instalación

Descarga la última versión desde la sección [Releases](https://github.com/Double-TK/Klavaranto/releases) de GitHub. Hay dos opciones:

* **Portable** (`Klavaranto_v1.1.2_portable.zip`) — descomprime el archivo y ejecuta `Klavaranto.exe` directamente, sin instalar nada.
* **Instalador** (`Klavaranto_v1.1.2-setup.exe`) — instala el programa con accesos directos en el menú inicio y el escritorio, e incluye desinstalador.

## Uso

Ejecuta `Klavaranto.exe`. Aparecerá un ícono en la bandeja del sistema — haz clic derecho para activar, configurar o salir.

Una vez activado, simplemente escribe normalmente: al completar una combinación, esta se reemplaza automáticamente por el carácter especial. Por ejemplo, al escribir `cx` se convierte en `ĉ`.

Si te equivocas, puedes deshacer el último cambio repitiendo el afijo o usando una tecla personalizada (configurable en Opciones).

En la ventana de Opciones puedes ajustar el método de entrada (prefijo, sufijo o doble tecla), el idioma de la interfaz, el atajo de activación, y si el programa inicia junto con Windows.

## Contribuir

¿Encontraste un error o tienes una sugerencia? Abre un [Issue en GitHub](https://github.com/Double-TK/Klavaranto/issues).

Si quieres apoyar el desarrollo de Klavaranto, puedes hacerlo a través de [Ko-fi](https://ko-fi.com/doubletk).

## Información técnica

Klavaranto está hecho en Python, usando las siguientes librerías:

* **tkinter** — interfaz gráfica
* **pynput** — detección de teclado
* **pystray** — ícono en la bandeja del sistema
* **Pillow** — generación de íconos y banderas

## Política de firma de código

Este proyecto está postulando al programa de SignPath Foundation para firma de código gratuita en binarios de Windows.

Estado: Pendiente de aprobación.

Si es aprobado: "Firma de código gratuita proporcionada por SignPath.io, certificado de SignPath Foundation"

Proceso de build: los binarios se compilan desde este repositorio usando GitHub Actions (ver `.github/workflows/compilar.yml`). Solo los artefactos compilados por este proceso automatizado serán enviados a firmar.

Roles: Gonzalo AB (Doble TK) es Autor, Revisor y Aprobador — único desarrollador del proyecto.

Privacidad: Este programa no recolecta ni transmite ningún dato del usuario. Toda la configuración y los registros (logs) se guardan localmente en el dispositivo del usuario.

---

## EO | Esperanto

## Karakterizaĵoj

* Konvertas klavkombinojn al specialaj Esperantaj signoj (cx→ĉ, gx→ĝ, hx→ĥ, jx→ĵ, sx→ŝ, ux→ŭ)
* Agordeblaj enigaj metodoj: prefikso, sufikso aŭ duobla klavo
* Sistemo por malfari — ripetante la afikson aŭ per propra klavo
* Agordebla aktiviga klavkombino, funkcias eĉ se modifaj klavoj restas "algluitaj"
* Plurlingva interfaco: Español, English, Esperanto
* Opcio por starti la programon jam aktiva
* Opcio por starti kun Vindozo
* Ikono en la sistema trako kun rapida menuo

## Instalado

Elŝutu la lastan version el la sekcio [Releases](https://github.com/Double-TK/Klavaranto/releases) en GitHub. Estas du opcioj:

* **Portebla** (`Klavaranto_v1.1.2_portable.zip`) — malzipu la dosieron kaj rulu `Klavaranto.exe` rekte, sen instalado.
* **Instalilo** (`Klavaranto_v1.1.2-setup.exe`) — instalas la programon kun ŝparvojoj en la komenca menuo kaj la labortablo, kaj inkluzivas malinstalilon.

## Uzado

Rulu `Klavaranto.exe`. Aperos ikono en la sistema trako — dekstre alklaku por aktivigi, agordi aŭ eliri.

Kiam aktiva, simple tajpu normale: kiam kombino estas kompletigita, ĝi aŭtomate anstataŭiĝas per la speciala signo. Ekzemple, tajpante `cx` ĝi fariĝas `ĉ`.

Se vi eraras, vi povas malfari la lastan ŝanĝon ripetante la afikson aŭ uzante propran klavon (agordebla en Agordoj).

En la fenestro Agordoj vi povas alĝustigi la enigan metodon (prefikso, sufikso aŭ duobla klavo), la lingvon de la interfaco, la aktivigan klavkombinon, kaj ĉu la programo startas kun Vindozo.

## Teknika informo

Klavaranto estas farita en Python, uzante la jenajn bibliotekojn:

* **tkinter** — grafika interfaco
* **pynput** — klavardetekto
* **pystray** — ikono en la sistema trako
* **Pillow** — generado de ikonoj kaj flagoj

## Kontribui

Ĉu vi trovis eraron aŭ havas sugeston? Malfermu [Issue en GitHub](https://github.com/Double-TK/Klavaranto/issues).

Se vi volas subteni la programadon de Klavaranto, vi povas fari tion per [Ko-fi](https://ko-fi.com/doubletk).

## Politiko pri kodsignado

Ĉi tiu projekto kandidatiĝas al la programo de SignPath Foundation por senpaga kodsignado de Vindozaj binaroj.

Stato: Atendante aprobon.

Se aprobita: "Senpaga kodsignado provizita de SignPath.io, atestilo de SignPath Foundation"

Konstruprocezo: la binaroj estas kompilitaj el ĉi tiu deponejo per GitHub Actions (vidu `.github/workflows/compilar.yml`). Nur artefaktoj konstruitaj per ĉi tiu aŭtomatigita procezo estos senditaj por subskribo.

Roloj: Gonzalo AB (Doble TK) estas Aŭtoro, Reviziisto kaj Aprobanto — sola programisto de la projekto.

Privateco: Ĉi tiu programo ne kolektas nek transdonas iujn ajn datumojn de la uzanto. Ĉiuj agordoj kaj protokoloj estas konservitaj loke sur la aparato de la uzanto.

---

## EN | English

## Features

* Converts key combinations into special Esperanto characters (cx→ĉ, gx→ĝ, hx→ĥ, jx→ĵ, sx→ŝ, ux→ŭ)
* Configurable input methods: prefix, suffix or double key
* Undo system — by repeating the affix or with a custom key
* Configurable activation shortcut, works even if modifier keys get "stuck"
* Multi-language interface: Español, English, Esperanto
* Option to start the program already enabled
* Option to start with Windows
* System tray icon with quick menu

## Installation

Download the latest version from the [Releases](https://github.com/Double-TK/Klavaranto/releases) section on GitHub. There are two options:

* **Portable** (`Klavaranto_v1.1.2_portable.zip`) — unzip the file and run `Klavaranto.exe` directly, no installation needed.
* **Installer** (`Klavaranto_v1.1.2-setup.exe`) — installs the program with shortcuts in the start menu and desktop, and includes an uninstaller.

## Usage

Run `Klavaranto.exe`. An icon will appear in the system tray — right-click to enable, configure or exit.

Once enabled, just type normally: when a combination is completed, it's automatically replaced by the special character. For example, typing `cx` becomes `ĉ`.

If you make a mistake, you can undo the last change by repeating the affix or using a custom key (configurable in Options).

In the Options window you can adjust the input method (prefix, suffix or double key), the interface language, the activation shortcut, and whether the program starts with Windows.

## Contributing

Found a bug or have a suggestion? Open an [Issue on GitHub](https://github.com/Double-TK/Klavaranto/issues).

If you want to support Klavaranto's development, you can do so via [Ko-fi](https://ko-fi.com/doubletk).

## Technical information

Klavaranto is made in Python, using the following libraries:

* **tkinter** — graphical interface
* **pynput** — keyboard detection
* **pystray** — system tray icon
* **Pillow** — icon and flag generation

## Code signing policy

This project is applying to the SignPath Foundation program for free code signing of Windows binaries.

Status: Pending approval.

If approved: "Free code signing provided by SignPath.io, certificate by SignPath Foundation"

Build process: binaries are built from this repository using GitHub Actions (see `.github/workflows/compilar.yml`). Only CI-built artifacts will be submitted to SignPath for signing.

Roles: Gonzalo AB (Doble TK) is Author, Reviewer, and Approver — the project's sole developer.

Privacy: This program does not collect or transmit any user data. All configuration and logs are stored locally on the user's device.

---

## Third-party licenses

* **pynput** — licensed under LGPL
* **pystray** — licensed under LGPL
* **Pillow** — licensed under the [MIT-CMU License](https://github.com/python-pillow/Pillow/blob/main/LICENSE)
* **Protest Riot font** — © Octavio Pardo, licensed under the [SIL Open Font License](https://scripts.sil.org/OFL)

---

© 2026 GAB. Klavaranto is free software, licensed under [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.html).

🔗 [GitHub](https://github.com/Double-TK/Klavaranto) | [Report a bug](https://github.com/Double-TK/Klavaranto/issues) | [Ko-fi](https://ko-fi.com/doubletk)
