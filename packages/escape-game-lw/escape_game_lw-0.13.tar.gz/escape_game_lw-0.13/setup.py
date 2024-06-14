from distutils.core import setup
setup(
  name = 'escape_game_lw',         # How you named your package folder (MyLib)
  packages = ['escape_game_lw'],   # Chose the same as "name"
  version = '0.13',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Basic functions for escape game',   # Give a short description about your library
  author = 'Luise Wiesalla',                   # Type in your name
  author_email = 'LuiseWiesalla@gmx.de',      # Type in your E-Mail
  url = 'https://github.com/Tchluwies/escape_game_lw',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Tchluwies/escape_game_lw/archive/refs/tags/0.12.tar.gz',    # I explain this later on
  keywords = ['Escape','Game'],   # Keywords that define your package best
  install_requires=[
      'numpy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)