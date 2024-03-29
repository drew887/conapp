# conapp - The easy config applier

A simple project for applying config files from repos/tar files

#### Example command:
```
conapp config -u drew887 -b
```

The above will:
  * download a tarball from drew887's config repo on bitbucket *(-b)*
  * take a backup of all the files that are listed in the tarball that
  would be overridden locally on your system. 
  * untar the repo into your home directory.

### Available commands:

#### `config` Command
Used for downloading and applying configs from either Bitbucket or Github.

  * `list`: Lists out configs that are available locally
  * `apply`: Download and apply a config based on username & repo name
  * `undo`: Remove files added by this config and apply last backup taken during
  its last application

      IE: `conapp config undo -u drew887` will:
       * delete all files listed in the currently downloaded config
       * apply the backup snapshot taken when the `drew887/config` repo was last applied


#### `snapshots` Command
Used for managing local backups created by conapp during the `config` commands

Available sub commands:
  * `list`: List available backups
  * `apply`: Restore a backup
  * `delete`: Delete a backup

#### `local` Command
Used to checkout a bare repo and print out a shell (bash for now sorry!) alias to simplify the use of the repo.
See https://www.atlassian.com/git/tutorials/dotfiles for more details on how this can be used.

The basic idea is that it can be used to check out a config but have it be managed by git without clobbering your home 
folder with a `.git` folder.

Available sub commands:
  * `checkout` Checkout a bare repo into `$XDG_CONFIG_HOME/conapp/local/repo`
  * `alias` prints out an alias to make using the bare repo easier  

##### Example usage:
```shell script
#check out the repo
conapp local checkout -b -u drew887
#setup the alias
conapp local info >> ~/.bashrc
#Now you can manage the repo with regular git commands aliased by default to `config`
config status
#regular git output here
```
Note that you'll probably want to run `checkout`
