import geopandas as gpd
import matplotlib.pyplot as plt

# US States geometryをロード
us_states = gpd.read_file('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json')

def get_user_input():
    """
    ユーザーから州とカラーの入力を取得します。
    """
    state_colors = {}
    while True:
        state = input("Enter state name (or 'done' to finish): ")
        if state.lower() == 'done':
            break
        color = input(f"Enter color for {state}: ")
        state_colors[state] = color
    return state_colors

def plot_us_states(state_colors):
    """
    入力された州とカラーの辞書を使用してUS Statesをプロットします。
    """
    # Apply the colors to the states, defaulting to light gray
    us_states['color'] = us_states['name'].map(lambda x: state_colors.get(x, 'lightgray'))

    # Plot the map
    fig, ax = plt.subplots(1, 1)
    us_states.plot(color=us_states['color'], ax=ax)
    plt.show()

# ユーザーからの入力を取得
user_state_colors = get_user_input()

# 入力に基づいて地図をプロット
plot_us_states(user_state_colors)
