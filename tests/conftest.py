from hypothesis import settings, Verbosity

settings.register_profile('trial',
                          # max_examples=100,
                          verbosity=Verbosity.verbose)
settings.load_profile('trial')
