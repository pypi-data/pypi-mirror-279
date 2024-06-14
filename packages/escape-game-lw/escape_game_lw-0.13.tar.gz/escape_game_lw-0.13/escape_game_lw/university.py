class university_data():
  def get(self, countries : list=['germany','austria','switzerland']):
    import requests

    data = []

    for country in countries:
      url = 'http://universities.hipolabs.com/search?country=' + country
      response = requests.get(url)
      if response.status_code == 200:
        data = data + response.json()

    return data