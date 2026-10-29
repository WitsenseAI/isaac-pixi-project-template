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

## Start a new project from the template

Do steps 1 to 3 above once on each machine. Also set up the Witsense
development standards once, as described in the README of
[witsense-dev-standards](https://github.com/WitsenseAI/witsense-dev-standards).
That installs `ruff` and `pre-commit`.

### 1. Create the repository

On the [template's GitHub page](https://github.com/WitsenseAI/isaac-pixi-project-template),
click **Use this template**, then **Create a new repository**. Set
**Owner** to WitsenseAI, name the project, and choose Public or Private.

With the GitHub CLI installed, this command does the same:

```bash
gh repo create WitsenseAI/<project-name> --template WitsenseAI/isaac-pixi-project-template --private --clone
```

### 2. Clone and install

```bash
git clone https://github.com/WitsenseAI/<project-name>.git
cd <project-name>
pixi install
pixi run check
pre-commit install
```

`pre-commit install` makes every commit run ruff first. A commit that
fails the checks is stopped.

### 3. Make it your project

- Change `name` and `description` in `pixi.toml`.
- Change the title and description in `README.md`.
- Replace the clone URL in step 4 of this file with your repository's URL.

Commit and push these changes.

### 4. Add code and packages

- Put scripts in `scripts/`. Each one starts with a one-line docstring and
  the `pixi run` command that launches it. Add a task for each script
  under `[tasks]` in `pixi.toml`.
- Add conda packages with `pixi add <package>` and PyPI packages with
  `pixi add --pypi <package>`. Both update `pixi.toml` and `pixi.lock`.
  Commit the two files together, because `pixi.lock` is what keeps every
  machine on the same versions.

### Joining an existing project

Clone the project's repository, then run `pixi install`, `pixi run check`
and `pre-commit install`. `pixi.lock` gives you the same versions as the
rest of the team.

### Template updates

A repository created from the template is an independent copy with its
own history. Later fixes to the template do not reach it. To pick one up,
copy the change across by hand.

## Move an existing project to this template

Work on a branch, and run these commands in Git Bash from your project's
root.

1. Copy the template files. `cp -n` never overwrites a file you already
   have.

   ```bash
   T=~/workspace/isaac-pixi-project-template
   cp -n $T/{pixi.toml,setup.md,CLAUDE.md,STYLE.md,ruff.toml,.pre-commit-config.yaml} .
   mkdir -p scripts .claude && cp -n $T/scripts/check_install.py scripts/ && cp -n $T/.claude/settings.json .claude/
   ```

   Merge `.gitattributes` and `.gitignore` from the template by hand. Do
   not copy `pixi.lock`; step 3 creates a new one.
2. Edit `pixi.toml`:
   - Set `name` and `description`.
   - Add your dependencies with `pixi add <package>` or
     `pixi add --pypi <package>`. Skip `isaacsim`, `isaaclab` and `torch`.
   - If your code is an installable package, add it as
     `my_project = { path = "source/my_project", editable = true }` under
     `[pypi-dependencies]`.
   - Add a task for each command you run.
3. Run `pixi install`, `pixi run check` and your own tasks. Code written
   for older Isaac versions may need updating, for example `omni.isaac.*`
   imports that moved to `isaacsim.*`.
4. Run `pre-commit install` and `ruff check .`, and fix what it reports.
5. Delete the old environment files, such as `requirements.txt` or
   `environment.yml`. Run `git add --renormalize .`, then commit,
   including `pixi.lock`.

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
