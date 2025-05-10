import requests
import plotly.express as px

# Make an API call and check the response.
url = "https://api.github.com/search/repositories"
url += "?q=language:java+sort:stars+stars:>10000"
headers = {"Accept": "application/vnd.github.v3+json"}

try:
    r = requests.get(url, headers=headers)
    r.raise_for_status() # raise an exception for bad status codes
    print(f"Status code: {r.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error during API request: {e}")
    exit()

# Process overall results
response_dict = r.json()
print(f"Complete results: {not response_dict['incomplete_results']}")

# Process repository information.
repo_dicts = response_dict['items']
repo_links, stars, hover_texts = [], [], []
for repo_dict in repo_dicts:
    # Turn repo names into active links.
    repo_name = repo_dict.get('name', 'No Name Available')
    repo_url = repo_dict.get('html_url', '#')
    repo_link = f"<a href='{repo_url}'>{repo_name}</a>"
    repo_links.append(repo_link)

    stars_count = repo_dict.get('stargazers_count', 0)
    stars.append(stars_count)

    # Build hover texts.
    owner_data = repo_dict.get('owner', {})
    owner = owner_data.get('login', 'Unknown Owner')
    description = repo_dict.get('description', 'No Description provided')
    hover_text = f"{owner}<br />{description}"
    hover_texts.append(hover_text)

# Create visualization.
title = "Most-Starred Java Projects on GitHub"
labels = {'x': 'Repository', 'y': 'Stars'}
fig = px.bar(x=repo_links, y=stars, title=title, labels=labels,
             hover_name=hover_texts, color=stars,
             color_continuous_scale=px.colors.sequential.Viridis)

fig.update_layout(
                title_font_size=28,
                title_x=0.5,
                title_font_color='white',
                xaxis_title_font_size=20,
                yaxis_title_font_size=20,
                xaxis_tickangle=45,
                plot_bgcolor='black',
                paper_bgcolor='black',
                font_color='white',
                hoverlabel=dict(bgcolor="gray", font_color='white')
                )

fig.update_traces(opacity=0.7)

fig.show()
