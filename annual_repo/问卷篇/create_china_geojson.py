import json

# 创建一个简单的中国地图GeoJSON文件
china_provinces = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": province},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[]]  # 简化版，仅用于示例
            }
        }
        for province in [
            "北京", "上海", "天津", "重庆",
            "河北", "山西", "辽宁", "吉林", "黑龙江",
            "江苏", "浙江", "安徽", "福建", "江西", "山东",
            "河南", "湖北", "湖南", "广东", "海南",
            "四川", "贵州", "云南", "陕西", "甘肃",
            "青海", "台湾", "内蒙古", "广西", "西藏",
            "宁夏", "新疆"
        ]
    ]
}

# 保存为GeoJSON文件
with open('china.geojson', 'w', encoding='utf-8') as f:
    json.dump(china_provinces, f, ensure_ascii=False, indent=2) 