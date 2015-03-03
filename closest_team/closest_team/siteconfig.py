def update_config(config):
    # Ensure that the NEShpDowloader is put into the config's available
    # downloaders by importing it.
    from cartopy.io.shapereader import NEShpDownloader

    # Define the URL template.
    URL_template = ('https://github.com/nvkelso/natural-earth-vector/'
                    'raw/master/zips/{resolution}_{category}/'
                    'ne_{resolution}_{name}.zip')

    # Get hold of the default NE downloader, and update the URL template.
    downloader = config['downloaders'][('shapefiles', 'natural_earth')]
    downloader.url_template = URL_template
