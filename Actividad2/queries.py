# Consultas 1 a 5 del proyecto BDAutos
#Consulta 1
def consulta_1(db):
    return list(db.cars.find(
        {
            "year": {"$gte": 2024},
            "mpg": {"$gte": 35}
        },
        {
            "_id": 0,
            "description": 1,
            "year": 1,
            "mpg": 1
        }
    ).sort("mpg", -1))

#Consulta 2
def consulta_2(db):
    return list(db.cars.find(
        {
            "continent.name": "europe",
            "cylinders": 4,
            "horsepower": {"$gte": 250}
        },
        {
            "_id": 0,
            "description": 1,
            "country.name": 1,
            "horsepower": 1
        }
    ).sort("horsepower", -1))

#Consulta 3
def consulta_3(db):
    pipeline = [
        {
            "$match": {
                "country.name": "japan",
                "description": {
                    "$regex": r"[0-9.]+t$",
                    "$options": "i"
                }
            }
        },
        {
            "$group": {
                "_id": "$makerId",
                "manufacturer": {"$first": "$maker.name"}
            }
        },
        {
            "$count": "fabricantesTurbo"
        }
    ]

    return list(db.cars.aggregate(pipeline))

#Consulta 4
def consulta_4(db):
    return list(db.cars.find(
        {
            "$or": [
                {
                    "weight": {"$lt": 3000},
                    "accel": {"$lt": 9}
                },
                {
                    "cylinders": {"$gte": 8},
                    "mpg": {"$gte": 19}
                }
            ]
        },
        {
            "_id": 0,
            "description": 1,
            "weight": 1,
            "accel": 1,
            "cylinders": 1,
            "mpg": 1
        }
    ))

#Consulta 5
def consulta_5(db):
    pipeline = [
        {
            "$lookup": {
                "from": "makers",
                "localField": "makerId",
                "foreignField": "_id",
                "as": "maker"
            }
        },
        {"$unwind": "$maker"},
        {
            "$lookup": {
                "from": "countries",
                "localField": "maker.countryId",
                "foreignField": "_id",
                "as": "country"
            }
        },
        {"$unwind": "$country"},
        {
            "$group": {
                "_id": "$maker._id",
                "manufacturer": {"$first": "$maker.name"},
                "country": {"$first": "$country.name"},
                "models": {"$addToSet": "$name"},
                "modelCount": {"$sum": 1}
            }
        },
        {
            "$match": {
                "modelCount": {"$gt": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "manufacturer": 1,
                "country": 1,
                "models": 1
            }
        }
    ]

    return list(db.models.aggregate(pipeline))

# Consultas 6 a 10 del proyecto BDAutos  
# Consulta 6: Autos cuya marca es distinta del fabricante
def consulta_6(db):
    return list(db.cars.find(
        {
            "$expr": {
                "$ne": ["$model.name", "$maker.name"]
            }
        },
        {
            "_id": 0,
            "description": 1,
            "model.name": 1,
            "maker.name": 1
        }
    ))

# Consulta 7: Estadisticas por pais
def consulta_7(db):
    pipeline = [
        {
            "$group": {
                "_id": "$country.name",
                "cars": {"$sum": 1},
                "averageMpg": {"$avg": "$mpg"},
                "averageHp": {"$avg": "$horsepower"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "country": "$_id",
                "cars": 1,
                "averageMpg": {"$round": ["$averageMpg", 1]},
                "averageHp": {"$round": ["$averageHp", 1]}
            }
        },
        {"$sort": {"cars": -1}}
    ]
    return list(db.cars.aggregate(pipeline))

# Consulta 8: Estadisticas por grupo fabricante
def consulta_8(db):
    pipeline = [
        {
            "$group": {
                "_id": "$makerId",
                "manufacturer": {"$first": "$maker.name"},
                "cars": {"$sum": 1},
                "brands": {"$addToSet": "$model.name"},
                "averageHp": {"$avg": "$horsepower"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "manufacturer": 1,
                "cars": 1,
                "distinctBrands": {"$size": "$brands"},
                "averageHp": {"$round": ["$averageHp", 1]}
            }
        },
        {"$sort": {"cars": -1}}
    ]
    return list(db.cars.aggregate(pipeline))

# Consulta 9: Modelos y marcas por continente
def consulta_9(db):
    pipeline = [
        {
            "$lookup": {
                "from": "makers",
                "localField": "makerId",
                "foreignField": "_id",
                "as": "maker"
            }
        },
        {"$unwind": "$maker"},
        {
            "$lookup": {
                "from": "countries",
                "localField": "maker.countryId",
                "foreignField": "_id",
                "as": "country"
            }
        },
        {"$unwind": "$country"},
        {
            "$group": {
                "_id": "$country.continent.name",
                "models": {"$addToSet": "$_id"},
                "brands": {"$addToSet": "$name"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "continent": "$_id",
                "models": {"$size": "$models"},
                "brands": {"$size": "$brands"}
            }
        },
        {"$sort": {"continent": 1}}
    ]
    return list(db.models.aggregate(pipeline))

# Consulta 10: Autos agrupados por rangos de MPG
def consulta_10(db):
    pipeline = [
        {
            "$bucket": {
                "groupBy": "$mpg",
                "boundaries": [0, 20, 25, 30, 35, 40],
                "default": "40+",
                "output": {
                    "count": {"$sum": 1},
                    "averageWeight": {"$avg": "$weight"}
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "range": "$_id",
                "count": 1,
                "averageWeight": {
                    "$round": ["$averageWeight", 1]
                }
            }
        }
    ]
    return list(db.cars.aggregate(pipeline))
    
# Consultas 11 a 15 del proyecto BDAutos
# Consulta 11: Cinco fabricantes con mayor MPG promedio
def consulta_11(db):
    pipeline = [
        {
            "$group": {
                "_id": "$makerId",
                "manufacturer": {"$first": "$maker.name"},
                "cars": {"$sum": 1},
                "averageMpg": {"$avg": "$mpg"}
            }
        },
        {"$match": {"cars": {"$gte": 8}}},
        {"$sort": {"averageMpg": -1}},
        {"$limit": 5},
        {
            "$project": {
                "_id": 0,
                "manufacturer": 1,
                "cars": 1,
                "averageMpg": {"$round": ["$averageMpg", 1]}
            }
        }
    ]
    return list(db.cars.aggregate(pipeline))

# Consulta 12: Categorias de rendimiento por continente
def consulta_12(db):
    pipeline = [
        {
            "$project": {
                "continent": "$continent.name",
                "category": {
                    "$switch": {
                        "branches": [
                            {
                                "case": {"$gte": ["$mpg", 30]},
                                "then": "Alta"
                            },
                            {
                                "case": {"$gte": ["$mpg", 20]},
                                "then": "Media"
                            }
                        ],
                        "default": "Baja"
                    }
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "continent": "$continent",
                    "category": "$category"
                },
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "continent": "$_id.continent",
                "category": "$_id.category",
                "count": 1
            }
        },
        {"$sort": {"continent": 1, "category": 1}}
    ]
    return list(db.cars.aggregate(pipeline))

# Consulta 13: Fabricantes incluidos los que tienen cero autos
def consulta_13(db):
    pipeline = [
        {
            "$lookup": {
                "from": "cars",
                "localField": "_id",
                "foreignField": "makerId",
                "as": "cars"
            }
        },
        {
            "$project": {
                "_id": 0,
                "manufacturer": "$name",
                "registeredCars": {"$size": "$cars"}
            }
        },
        {"$sort": {"registeredCars": -1}}
    ]
    return list(db.makers.aggregate(pipeline))

# Consulta 14: Modelos sin autos registrados
def consulta_14(db):
    pipeline = [
        {
            "$lookup": {
                "from": "cars",
                "localField": "_id",
                "foreignField": "modelId",
                "as": "cars"
            }
        },
        {
            "$match": {
                "$expr": {
                    "$eq": [{"$size": "$cars"}, 0]
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "modelId": "$_id",
                "model": "$name",
                "makerId": 1
            }
        }
    ]
    return list(db.models.aggregate(pipeline))

# Consulta 15: Cinco autos mas potentes
def consulta_15(db):
    pipeline = [
        {"$sort": {"horsepower": -1}},
        {"$limit": 5},
        {
            "$project": {
                "_id": 0,
                "description": 1,
                "horsepower": 1,
                "manufacturer": "$maker.fullName"
            }
        }
    ]
    return list(db.cars.aggregate(pipeline))
    
# Consultas 16 a 20 del proyecto BDAutos
# Consulta 16: Tres autos mas eficientes por continente
def consulta_16(db):
    pipeline = [
        {"$sort": {"continent.name": 1, "mpg": -1}},
        {
            "$group": {
                "_id": "$continent.name",
                "cars": {
                    "$push": {
                        "description": "$description",
                        "mpg": "$mpg"
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "continent": "$_id",
                "cars": {"$slice": ["$cars", 3]}
            }
        }
    ]
    return list(db.cars.aggregate(pipeline))

# Consulta 17: Modelo con mas autos por fabricante
def consulta_17(db):
    pipeline = [
        {
            "$group": {
                "_id": {
                    "makerId": "$makerId",
                    "modelId": "$modelId"
                },
                "manufacturer": {"$first": "$maker.name"},
                "model": {"$first": "$model.name"},
                "cars": {"$sum": 1}
            }
        },
        {"$sort": {"_id.makerId": 1, "cars": -1}},
        {
            "$group": {
                "_id": "$_id.makerId",
                "manufacturer": {"$first": "$manufacturer"},
                "model": {"$first": "$model"},
                "cars": {"$first": "$cars"},
                "modelCount": {"$sum": 1}
            }
        },
        {"$match": {"modelCount": {"$gt": 1}}},
        {
            "$project": {
                "_id": 0,
                "manufacturer": 1,
                "model": 1,
                "cars": 1
            }
        }
    ]
    return list(db.cars.aggregate(pipeline))

# Consulta 18: Porcentaje de autos por continente
def consulta_18(db):
    pipeline = [
        {
            "$group": {
                "_id": "$continent.name",
                "cars": {"$sum": 1}
            }
        },
        {
            "$group": {
                "_id": None,
                "total": {"$sum": "$cars"},
                "continents": {
                    "$push": {
                        "continent": "$_id",
                        "cars": "$cars"
                    }
                }
            }
        },
        {"$unwind": "$continents"},
        {
            "$project": {
                "_id": 0,
                "continent": "$continents.continent",
                "cars": "$continents.cars",
                "percentage": {
                    "$round": [
                        {
                            "$multiply": [
                                {"$divide": ["$continents.cars", "$total"]},
                                100
                            ]
                        },
                        2
                    ]
                }
            }
        }
    ]
    return list(db.cars.aggregate(pipeline))

# Consulta 19: Cinco autos que mas superan el promedio de MPG
# de los autos con la misma cantidad de cilindros
def consulta_19(db):
    pipeline = [
        {
            "$group": {
                "_id": "$cylinders",
                "averageMpg": {"$avg": "$mpg"},
                "cars": {"$push": "$$ROOT"}
            }
        },
        {"$unwind": "$cars"},
        {
            "$project": {
                "_id": 0,
                "description": "$cars.description",
                "cylinders": "$_id",
                "mpg": "$cars.mpg",
                "averageMpg": 1,
                "difference": {
                    "$subtract": ["$cars.mpg", "$averageMpg"]
                }
            }
        },
        {"$sort": {"difference": -1}},
        {"$limit": 5}
    ]
    return list(db.cars.aggregate(pipeline))

# Consulta 20: Autos con ocho o mas cilindros por continente
def consulta_20(db):
    pipeline = [
        {
            "$group": {
                "_id": "$continent.name",
                "totalCars": {"$sum": 1},
                "highCylinders": {
                    "$sum": {
                        "$cond": [
                            {"$gte": ["$cylinders", 8]},
                            1,
                            0
                        ]
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "continent": "$_id",
                "totalCars": 1,
                "highCylinders": 1,
                "percentage": {
                    "$round": [
                        {
                            "$multiply": [
                                {"$divide": ["$highCylinders", "$totalCars"]},
                                100
                            ]
                        },
                        1
                    ]
                }
            }
        }
    ]
    return list(db.cars.aggregate(pipeline))

# Consultas 21 a 25 del proyecto BDAutos
# Consulta 21: Potencia por cada 1000 libras
def consulta_21(db):
    pipeline = [
        {
            "$project": {
                "_id": 0,
                "description": 1,
                "horsepower": 1,
                "weight": 1,
                "country": "$country.name",
                "hpPer1000lb": {
                    "$divide": [
                        "$horsepower",
                        {"$divide": ["$weight", 1000]}
                    ]
                }
            }
        },
        {"$sort": {"hpPer1000lb": -1}},
        {"$limit": 10}
    ]
    return list(db.cars.aggregate(pipeline))

# Consulta 22: Modelos distintos del nombre del fabricante
def consulta_22(db):
    pipeline = [
        {
            "$lookup": {
                "from": "makers",
                "localField": "makerId",
                "foreignField": "_id",
                "as": "maker"
            }
        },
        {"$unwind": "$maker"},
        {
            "$match": {
                "$expr": {"$ne": ["$name", "$maker.name"]}
            }
        },
        {
            "$project": {
                "_id": 0,
                "manufacturer": "$maker.name",
                "model": "$name"
            }
        }
    ]
    return list(db.models.aggregate(pipeline))

# Consulta 23: Resumen general de la base de datos
def consulta_23(db):
    pipeline = [
        {
            "$facet": {
                "carsByContinent": [
                    {
                        "$group": {
                            "_id": "$continent.name",
                            "cars": {"$sum": 1}
                        }
                    }
                ],
                "carsByCylinders": [
                    {
                        "$group": {
                            "_id": "$cylinders",
                            "cars": {"$sum": 1}
                        }
                    },
                    {"$sort": {"_id": 1}}
                ],
                "globalMpg": [
                    {
                        "$group": {
                            "_id": None,
                            "min": {"$min": "$mpg"},
                            "max": {"$max": "$mpg"},
                            "average": {"$avg": "$mpg"}
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "min": 1,
                            "max": 1,
                            "average": {"$round": ["$average", 1]}
                        }
                    }
                ]
            }
        }
    ]
    return list(db.cars.aggregate(pipeline))

# Consulta 24: Ranking de los cinco autos alemanes mas potentes
def consulta_24(db):
    pipeline = [
        {"$match": {"country.name": "germany"}},
        {
            "$setWindowFields": {
                "partitionBy": "$country.name",
                "sortBy": {"horsepower": -1},
                "output": {"rank": {"$rank": {}}}
            }
        },
        {"$match": {"rank": {"$lte": 5}}},
        {
            "$project": {
                "_id": 0,
                "rank": 1,
                "description": 1,
                "horsepower": 1
            }
        }
    ]
    return list(db.cars.aggregate(pipeline))

# Consulta 25: Auto mas eficiente de cada fabricante europeo
def consulta_25(db):
    pipeline = [
        {"$match": {"continent.name": "europe"}},
        {"$sort": {"makerId": 1, "mpg": -1}},
        {
            "$group": {
                "_id": "$makerId",
                "manufacturer": {"$first": "$maker.name"},
                "country": {"$first": "$country.name"},
                "description": {"$first": "$description"},
                "mpg": {"$first": "$mpg"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "manufacturer": 1,
                "country": 1,
                "description": 1,
                "mpg": 1
            }
        },
        {"$sort": {"mpg": -1}}
    ]
    return list(db.cars.aggregate(pipeline))