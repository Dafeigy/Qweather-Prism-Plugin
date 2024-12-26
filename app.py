from flask import Flask, jsonify, render_template
import requests
import os
app = Flask(__name__)

KEY = os.environ['KEY']

# # 路由：获取所有数据
# @app.route('/geoid', methods=['GET'])
# def get_data():
#     return jsonify(data)

@app.route("/",methods=['GET'])
def main_page():
    return render_template("index.html")

# 路由：根据 ID 获取单个数据
@app.route('/geoid/<string:city_name>', methods=['GET'])
def get_single_data(city_name):
    geo_url = f"https://geoapi.qweather.com/v2/city/lookup?location={city_name}&key={KEY}"
    req = requests.get(geo_url)
    # print(req.json())
    res = req.json()
    if res['code'] == "200":
        city_id = res['location'][0]['id']
        return city_id
    else:
        return jsonify({"error": "Not found"}),404
@app.route("/qweather/<string:city_name>", methods = ['GET'])
def get_weather_data(city_name):
    geo_url = f"https://geoapi.qweather.com/v2/city/lookup?location={city_name}&key={KEY}"
    req = requests.get(geo_url)
    # print(req.json())
    res = req.json()
    if res['code'] == "200":
        city_id = res['location'][0]['id']
    else:
        return jsonify({"error": "Not found"}),404
    print(city_id)
    weather_url = f"https://devapi.qweather.com/v7/weather/now?location={city_id}&key={KEY}"
    req = requests.get(weather_url)
    # print(req.json())
    res = req.json()
    if res['code'] == "200":
        data = res['now']
        return jsonify({
            "更新时间":data['obsTime'],
            "体感温度":data["feelsLike"],
            "湿度":data['humidity'],
            "温度":data['temp'],
            "天气状况":data['text'],
            "能见度":data['vis']
        })
    else:
        return jsonify({"error": "Internal server error"}), 500

# # 路由：添加新数据
# @app.route('/api/data', methods=['POST'])
# def add_data():
#     new_item = request.get_json()
#     if not new_item or 'name' not in new_item or 'age' not in new_item:
#         return jsonify({"error": "Invalid data"}), 400
    
#     new_item['id'] = max(x['id'] for x in data) + 1
#     data.append(new_item)
#     return jsonify(new_item), 201


# 错误处理：404
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

# 错误处理：500
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)