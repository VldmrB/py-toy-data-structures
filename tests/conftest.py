from hypothesis import settings, Verbosity

settings.register_profile('trial',
                          max_examples=100,
                          verbosity=Verbosity.verbose)
settings.register_profile('quick',
                          max_examples=10,
                          verbosity=Verbosity.verbose)
settings.load_profile('quick')  # override with a manual command for Travis CI
