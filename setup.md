# Setup

This template installs Isaac Sim 6.2, Isaac Lab 3.0 and CUDA PyTorch with a
single `pixi install`, on Windows and on Linux. Every machine gets the exact
versions recorded in `pixi.lock`.

## 1. Check your machine

| | Windows | Linux |
|---|---|---|
| OS | Windows 10 or 11, x86-64 | Ubuntu 22.04 or newer (glibc 2.35+), x86-64 |
| GPU | NVIDIA RTX GPU | NVIDIA RTX GPU |
| Driver | Supports CUDA 12 or newer | Supports CUDA 12 or newer |
| Disk | Tens of GB free for the environment and the pixi cache | Same |

macOS is not supported, because Isaac Sim does not run on it.

To check the driver, run `nvidia-smi`. The `CUDA Version` in its header
must be 12.0 or higher. If it is lower, update the NVIDIA driver first.

For NVIDIA's full hardware requirements, see the Isaac Sim documentation.

## 2. Windows only: enable long paths

Isaac Sim installs files with very long paths. Without long path support,
the install fails partway through. In a PowerShell window run as
Administrator:

```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
git config --global core.longpaths true
```

Then restart Windows.

## 3. Install pixi

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"
```

Linux:

```bash
curl -fsSL https://pixi.sh/install.sh | sh
```

Open a new terminal, then check that `pixi --version` prints a version.
The manifest uses the platform syntax from pixi 0.81, so update older
installs with `pixi self-update`.

## 4. Install the project

```bash
git clone https://github.com/WitsenseAI/isaac-pixi-project-template.git
cd isaac-pixi-project-template
pixi install
```

The first install downloads many gigabytes from NVIDIA's and PyTorch's
package indexes and can take a long time. Later installs on the same
machine reuse the pixi cache.

## 5. Check the install

```bash
pixi run check
```

This starts Isaac Sim without a window, loads Isaac Lab, and prints the
installed versions and your GPU. It exits with an error if PyTorch cannot
see CUDA. The first run is slow, because Isaac Sim builds its shader cache.

## NVIDIA license

`pixi.toml` sets `OMNI_KIT_ACCEPT_EULA=YES`, so Isaac Sim does not stop to
ask for license acceptance on first launch. Running the project therefore
accepts the NVIDIA Isaac Sim license on your behalf. Read that license, and
remove the setting if you would rather accept it when Isaac Sim asks.

## Start your own project from the template

1. Create a new repository from this template, or clone it and point
   `origin` at your own repository.
2. Change `name` and `description` in `pixi.toml`.
3. Put your scripts in `scripts/` and add a task for each one under
   `[tasks]` in `pixi.toml`.
4. Commit `pixi.lock`. It is what keeps every machine on the same versions.

## Changing versions

Edit the version pins in `pixi.toml`, run `pixi lock`, check that
`pixi run check` still passes on Windows and on Linux, then commit both
`pixi.toml` and `pixi.lock`.

Three settings in `pixi.toml` work around problems in the published Isaac
packages. Check whether each one is still needed when you change versions:

- `dependency-overrides` for `urllib3`: Isaac Lab 3.0.0 requires urllib3
  2.8 or newer, while Isaac Sim 6.2.0.0 pins 2.7.0, so the two cannot be
  installed together without the override.
- `tinyobjloader = "==2.0.0rc13"`: Isaac Sim 6.2.0.0 depends on this
  pre-release. Listing it directly allows this one pre-release without
  allowing pre-releases for every package.
- `glibc = "2.35"` on the Linux platform: the Isaac Sim Linux wheels need
  glibc 2.35, and pixi has to be told the machine provides it.

## Troubleshooting

**`os error 1450` / "Insufficient system resources" on Windows.** Windows
ran out of memory while reading one of the very large Isaac Sim packages.
Close other programs and run the install again. If it still fails, enlarge
the Windows page file.

**"no wheels with a matching platform tag" on Linux.** The system glibc is
older than 2.35. Upgrade to Ubuntu 22.04 or newer.

**`CUDA: not available` from `pixi run check`.** The NVIDIA driver is
missing or too old. Check `nvidia-smi` as in step 1.
