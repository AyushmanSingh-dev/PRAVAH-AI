"""
Catchment physical, geotechnical, and river routing parameters for high-risk
Himalayan River Basins in Uttarakhand (Alaknanda, Mandakini, and Bhagirathi).
"""

HIMALAYAN_REGIONS = {
    "alaknanda": {
        "id": "alaknanda",
        "name": "Alaknanda & Rishi Ganga Basin",
        "short_name": "Alaknanda (Chamoli)",
        "district": "Chamoli, Uttarakhand",
        "state": "Uttarakhand",
        "elevation_range": "1,050m - 5,200m",
        "dominant_geology": "Crystalline Gneiss & Colluvial Debris Mantle",
        "catchment_area_km2": 85.0,
        "base_flow_m3s": 35.0,
        "center_lat": 30.49,
        "center_lon": 79.55,
        "default_zoom": 11,
        "river_path": [
            [30.4710, 79.7350], # High Alpine Glacier Headwater
            [30.4886, 79.6975], # Raini Village / Rishi Ganga Confluence
            [30.5012, 79.6241], # Tapovan Barrage Site
            [30.5310, 79.5880], # Dhauliganga Mid-Gorge
            [30.5567, 79.5684], # Vishnuprayag (Alaknanda Confluence)
            [30.5200, 79.5100], # Joshimath Lower Flank
            [30.4500, 79.4200], # Helang / Gulabkoti
            [30.4128, 79.3315]  # Chamoli Town / Bridge
        ],
        "geotechnical": {
            "c_prime": 8500.0,
            "phi_prime_deg": 32.0,
            "gamma_sat": 19500.0,
            "gamma_w": 9810.0,
            "soil_depth_z": 2.2,
            "slope_beta_deg": 35.0,
            "k_sat_mm_hr": 14.5,
            "psi_suction_mm": 110.0,
            "theta_sat": 0.44,
            "theta_init_default": 0.22
        },
        "hydraulic": {
            "manning_n": 0.048,
            "bed_slope_s0": 0.024,
            "bottom_width_b": 28.0,
            "side_slope_z": 1.2
        },
        "settlements": [
            {
                "id": "raini",
                "name": "Raini Village (Bridge)",
                "lat": 30.4886,
                "lon": 79.6975,
                "distance_km": 4.5,
                "elevation_m": 2040,
                "normal_depth_m": 1.8,
                "warning_depth_m": 3.6,
                "danger_depth_m": 4.8,
                "population": 1250,
                "priority": "CRITICAL"
            },
            {
                "id": "tapovan",
                "name": "Tapovan (Barrage & Settlement)",
                "lat": 30.5012,
                "lon": 79.6241,
                "distance_km": 12.8,
                "elevation_m": 1820,
                "normal_depth_m": 2.4,
                "warning_depth_m": 4.8,
                "danger_depth_m": 6.2,
                "population": 3400,
                "priority": "HIGH"
            },
            {
                "id": "vishnuprayag",
                "name": "Vishnuprayag Confluence",
                "lat": 30.5567,
                "lon": 79.5684,
                "distance_km": 25.2,
                "elevation_m": 1410,
                "normal_depth_m": 3.2,
                "warning_depth_m": 6.2,
                "danger_depth_m": 8.0,
                "population": 4800,
                "priority": "HIGH"
            },
            {
                "id": "chamoli",
                "name": "Chamoli / Joshimath Lower Reach",
                "lat": 30.4128,
                "lon": 79.3315,
                "distance_km": 44.0,
                "elevation_m": 1050,
                "normal_depth_m": 4.0,
                "warning_depth_m": 7.5,
                "danger_depth_m": 9.5,
                "population": 18500,
                "priority": "STRATEGIC"
            }
        ],
        "authority": {
            "ddma_name": "Chamoli District Disaster Management Authority (DDMA)",
            "siren_freq": "144.50 MHz VHF",
            "state_control": "Uttarakhand State Emergency Operation Centre (SEOC Dehradun)",
            "local_dialects": "Garhwali / Hindi"
        },
        "scenarios": {
            "chamoli_2021": {
                "name": "Chamoli 2021 Cloudburst & Debris Dam Breach",
                "rainfall_rate_mm_hr": 105.0,
                "duration_hr": 2.5,
                "initial_soil_moisture": 0.38,
                "description": "High-altitude rock/ice avalanche and moraine dam breach surging down Rishi Ganga."
            },
            "monsoon_saturated": {
                "name": "Active Monsoon Prolonged Saturated Slope Failure",
                "rainfall_rate_mm_hr": 52.0,
                "duration_hr": 12.0,
                "initial_soil_moisture": 0.42,
                "description": "Continuous multi-day rain drives regolith to saturation (AMC III), triggering Dunne runoff."
            },
            "normal_baseline": {
                "name": "Clear Weather Summer Baseline",
                "rainfall_rate_mm_hr": 4.0,
                "duration_hr": 1.0,
                "initial_soil_moisture": 0.20,
                "description": "Typical dry-season baseflow. Infiltration capacity safely absorbs precipitation."
            }
        }
    },

    "mandakini": {
        "id": "mandakini",
        "name": "Mandakini River Basin (Kedarnath Corridor)",
        "short_name": "Mandakini (Kedarnath)",
        "district": "Rudraprayag, Uttarakhand",
        "state": "Uttarakhand",
        "elevation_range": "610m - 4,100m",
        "dominant_geology": "Glacial Moraines, Paragneiss & High-Gradient Scree",
        "catchment_area_km2": 68.0,
        "base_flow_m3s": 40.0,
        "center_lat": 30.64,
        "center_lon": 79.05,
        "default_zoom": 11,
        "river_path": [
            [30.7450, 79.0700], # Chorabari Snout & Moraine Lake
            [30.7350, 79.0670], # Kedarnath Temple Township
            [30.6850, 79.0450], # Rambara Gorge
            [30.6520, 79.0300], # Gaurikund Hot Springs
            [30.6310, 78.9980], # Sonprayag Confluence
            [30.5500, 79.0500], # Kund / Phata Helipad Reach
            [30.4500, 79.0700], # Agastyamuni Floodplain
            [30.2850, 78.9800]  # Rudraprayag (Alaknanda Confluence)
        ],
        "geotechnical": {
            "c_prime": 6500.0,
            "phi_prime_deg": 30.0,
            "gamma_sat": 19200.0,
            "gamma_w": 9810.0,
            "soil_depth_z": 1.8,
            "slope_beta_deg": 38.0,
            "k_sat_mm_hr": 16.0,
            "psi_suction_mm": 95.0,
            "theta_sat": 0.44,
            "theta_init_default": 0.25
        },
        "hydraulic": {
            "manning_n": 0.052,
            "bed_slope_s0": 0.029,
            "bottom_width_b": 24.0,
            "side_slope_z": 1.2
        },
        "settlements": [
            {
                "id": "kedarnath_town",
                "name": "Kedarnath Township (Temple)",
                "lat": 30.7350,
                "lon": 79.0670,
                "distance_km": 1.5,
                "elevation_m": 3580,
                "normal_depth_m": 1.2,
                "warning_depth_m": 2.4,
                "danger_depth_m": 3.2,
                "population": 850,
                "priority": "CRITICAL"
            },
            {
                "id": "rambara",
                "name": "Rambara Gorge Crossing",
                "lat": 30.6850,
                "lon": 79.0450,
                "distance_km": 6.5,
                "elevation_m": 2700,
                "normal_depth_m": 1.8,
                "warning_depth_m": 3.5,
                "danger_depth_m": 4.5,
                "population": 450,
                "priority": "CRITICAL"
            },
            {
                "id": "gaurikund",
                "name": "Gaurikund Base Station",
                "lat": 30.6520,
                "lon": 79.0300,
                "distance_km": 12.0,
                "elevation_m": 1980,
                "normal_depth_m": 2.2,
                "warning_depth_m": 4.2,
                "danger_depth_m": 5.5,
                "population": 2200,
                "priority": "HIGH"
            },
            {
                "id": "sonprayag",
                "name": "Sonprayag Confluence & Bridge",
                "lat": 30.6310,
                "lon": 78.9980,
                "distance_km": 18.5,
                "elevation_m": 1650,
                "normal_depth_m": 2.8,
                "warning_depth_m": 5.2,
                "danger_depth_m": 6.8,
                "population": 3400,
                "priority": "HIGH"
            },
            {
                "id": "rudraprayag",
                "name": "Rudraprayag Sangam Bridge",
                "lat": 30.2850,
                "lon": 78.9800,
                "distance_km": 52.0,
                "elevation_m": 610,
                "normal_depth_m": 4.2,
                "warning_depth_m": 7.5,
                "danger_depth_m": 9.5,
                "population": 15500,
                "priority": "STRATEGIC"
            }
        ],
        "authority": {
            "ddma_name": "Rudraprayag District Disaster Management Authority (DDMA)",
            "siren_freq": "145.20 MHz VHF",
            "state_control": "Uttarakhand State Emergency Operation Centre (SEOC Dehradun)",
            "local_dialects": "Garhwali / Hindi"
        },
        "scenarios": {
            "kedarnath_2013": {
                "name": "Kedarnath 2013 Moraine Dam Breach (Chorabari GLOF)",
                "rainfall_rate_mm_hr": 85.0,
                "duration_hr": 4.0,
                "initial_soil_moisture": 0.42,
                "description": "Torrential 72-hr cloudburst saturates regolith; Chorabari moraine impoundment collapses releasing 2,850 m³/s wave."
            },
            "monsoon_mandakini": {
                "name": "Mandakini Active Monsoon Inundation Watch",
                "rainfall_rate_mm_hr": 48.0,
                "duration_hr": 8.0,
                "initial_soil_moisture": 0.38,
                "description": "Continuous Himalayan monsoon rains elevate water levels above the warning threshold at Gaurikund and Sonprayag."
            },
            "normal_baseline": {
                "name": "Clear Weather Baseflow Regime",
                "rainfall_rate_mm_hr": 3.5,
                "duration_hr": 1.0,
                "initial_soil_moisture": 0.22,
                "description": "Typical serene post-monsoon baseflow across the Kedarnath pilgrimage corridor."
            }
        }
    },

    "bhagirathi": {
        "id": "bhagirathi",
        "name": "Bhagirathi River Basin (Uttarkashi Reach)",
        "short_name": "Bhagirathi (Uttarkashi)",
        "district": "Uttarkashi, Uttarakhand",
        "state": "Uttarakhand",
        "elevation_range": "850m - 3,800m",
        "dominant_geology": "Weathered Biotite Schist, Quartzite & Valley Colluvium",
        "catchment_area_km2": 110.0,
        "base_flow_m3s": 45.0,
        "center_lat": 30.82,
        "center_lon": 78.60,
        "default_zoom": 10,
        "river_path": [
            [30.9950, 78.9400], # Gangotri Snout / Gaumukh Reach
            [31.0350, 78.7400], # Harsil Apple Valley
            [30.9100, 78.6700], # Maneri Dam Reach
            [30.8150, 78.6200], # Bhatwari Gushing Rapids
            [30.7250, 78.4400], # Uttarkashi Town / Tiloth Bridge
            [30.6500, 78.3900], # Dharasu Confluence
            [30.5600, 78.3300]  # Chinyalisaur (Tehri Dam Tailwaters)
        ],
        "geotechnical": {
            "c_prime": 7800.0,
            "phi_prime_deg": 33.0,
            "gamma_sat": 19400.0,
            "gamma_w": 9810.0,
            "soil_depth_z": 2.4,
            "slope_beta_deg": 33.0,
            "k_sat_mm_hr": 17.5,
            "psi_suction_mm": 100.0,
            "theta_sat": 0.44,
            "theta_init_default": 0.22
        },
        "hydraulic": {
            "manning_n": 0.046,
            "bed_slope_s0": 0.020,
            "bottom_width_b": 32.0,
            "side_slope_z": 1.3
        },
        "settlements": [
            {
                "id": "harsil",
                "name": "Harsil Valley & Army Camp",
                "lat": 31.0350,
                "lon": 78.7400,
                "distance_km": 8.0,
                "elevation_m": 2620,
                "normal_depth_m": 1.8,
                "warning_depth_m": 3.4,
                "danger_depth_m": 4.5,
                "population": 1900,
                "priority": "CRITICAL"
            },
            {
                "id": "bhatwari",
                "name": "Bhatwari River Bridge",
                "lat": 30.8150,
                "lon": 78.6200,
                "distance_km": 24.0,
                "elevation_m": 1220,
                "normal_depth_m": 2.4,
                "warning_depth_m": 4.6,
                "danger_depth_m": 6.0,
                "population": 3200,
                "priority": "HIGH"
            },
            {
                "id": "uttarkashi",
                "name": "Uttarkashi Town (Tiloth)",
                "lat": 30.7250,
                "lon": 78.4400,
                "distance_km": 46.0,
                "elevation_m": 1150,
                "normal_depth_m": 3.2,
                "warning_depth_m": 6.2,
                "danger_depth_m": 8.0,
                "population": 17500,
                "priority": "STRATEGIC"
            },
            {
                "id": "chinyalisaur",
                "name": "Chinyalisaur Airfield Reach",
                "lat": 30.5600,
                "lon": 78.3300,
                "distance_km": 72.0,
                "elevation_m": 850,
                "normal_depth_m": 4.0,
                "warning_depth_m": 7.2,
                "danger_depth_m": 9.2,
                "population": 9800,
                "priority": "HIGH"
            }
        ],
        "authority": {
            "ddma_name": "Uttarkashi District Disaster Management Authority (DDMA)",
            "siren_freq": "146.10 MHz VHF",
            "state_control": "Uttarakhand State Emergency Operation Centre (SEOC Dehradun)",
            "local_dialects": "Garhwali / Hindi"
        },
        "scenarios": {
            "uttarkashi_2012": {
                "name": "Uttarkashi 2012 Cloudburst Flash Surge (Asi Ganga)",
                "rainfall_rate_mm_hr": 95.0,
                "duration_hr": 3.0,
                "initial_soil_moisture": 0.40,
                "description": "Extreme Asi Ganga cloudburst funnelled boulders and debris into Bhagirathi river, sweeping Tiloth bridge."
            },
            "monsoon_bhagirathi": {
                "name": "Active Monsoon Riverbank Overflow Watch",
                "rainfall_rate_mm_hr": 45.0,
                "duration_hr": 10.0,
                "initial_soil_moisture": 0.38,
                "description": "High watershed rainfall increases Bhagirathi inflow into downstream Tehri reservoir buffer."
            },
            "normal_baseline": {
                "name": "Clear Weather Baseflow Regime",
                "rainfall_rate_mm_hr": 4.0,
                "duration_hr": 1.0,
                "initial_soil_moisture": 0.20,
                "description": "Normal glacial melt and clear-weather baseflow along the Uttarkashi riverbed."
            }
        }
    },

    "beas": {
        "id": "beas",
        "name": "Beas River Basin (Kullu - Manali Valley)",
        "short_name": "Beas (Kullu-Manali)",
        "district": "Kullu, Himachal Pradesh",
        "state": "Himachal Pradesh",
        "elevation_range": "1,100m - 4,200m",
        "dominant_geology": "Central Crystalline Gneiss, Quartzite & River Terraces",
        "catchment_area_km2": 95.0,
        "base_flow_m3s": 38.0,
        "center_lat": 31.95,
        "center_lon": 77.15,
        "default_zoom": 11,
        "river_path": [
            [32.3200, 77.1800], # Rohtang Pass / Solang Valley
            [32.2800, 77.1650], # Palchan Confluence
            [32.2432, 77.1892], # Old Manali Bridge
            [32.1800, 77.1700], # Patlikuhal Orchard Reach
            [31.9600, 77.1100], # Kullu Town (Akhara Bazar)
            [31.8600, 77.1400], # Bhuntar (Parbati Confluence)
            [31.7500, 77.1200], # Aut Gorge Entrance
            [31.6700, 77.0600]  # Pandoh Dam Spillway
        ],
        "geotechnical": {
            "c_prime": 7200.0,
            "phi_prime_deg": 32.0,
            "gamma_sat": 19300.0,
            "gamma_w": 9810.0,
            "soil_depth_z": 2.0,
            "slope_beta_deg": 34.0,
            "k_sat_mm_hr": 15.2,
            "psi_suction_mm": 105.0,
            "theta_sat": 0.43,
            "theta_init_default": 0.23
        },
        "hydraulic": {
            "manning_n": 0.045,
            "bed_slope_s0": 0.022,
            "bottom_width_b": 30.0,
            "side_slope_z": 1.2
        },
        "settlements": [
            {
                "id": "palchan",
                "name": "Palchan Village (Solang Confluence)",
                "lat": 32.2800,
                "lon": 77.1650,
                "distance_km": 3.5,
                "elevation_m": 2310,
                "normal_depth_m": 1.6,
                "warning_depth_m": 3.2,
                "danger_depth_m": 4.4,
                "population": 950,
                "priority": "CRITICAL"
            },
            {
                "id": "manali_town",
                "name": "Old Manali / Mall Road Bridge",
                "lat": 32.2432,
                "lon": 77.1892,
                "distance_km": 9.0,
                "elevation_m": 2050,
                "normal_depth_m": 2.2,
                "warning_depth_m": 4.2,
                "danger_depth_m": 5.6,
                "population": 8500,
                "priority": "CRITICAL"
            },
            {
                "id": "kullu_town",
                "name": "Kullu Town (Akhara Bazar)",
                "lat": 31.9600,
                "lon": 77.1100,
                "distance_km": 38.0,
                "elevation_m": 1220,
                "normal_depth_m": 3.4,
                "warning_depth_m": 6.5,
                "danger_depth_m": 8.5,
                "population": 18500,
                "priority": "STRATEGIC"
            },
            {
                "id": "pandoh",
                "name": "Pandoh Dam / Aut Reach",
                "lat": 31.6700,
                "lon": 77.0600,
                "distance_km": 68.0,
                "elevation_m": 880,
                "normal_depth_m": 4.5,
                "warning_depth_m": 8.0,
                "danger_depth_m": 10.5,
                "population": 6200,
                "priority": "HIGH"
            }
        ],
        "authority": {
            "ddma_name": "Kullu District Disaster Management Authority (DDMA)",
            "siren_freq": "147.30 MHz VHF",
            "state_control": "Himachal Pradesh State Disaster Management Authority (HPSDMA Shimla)",
            "local_dialects": "Kulluvi / Pahari / Hindi"
        },
        "scenarios": {
            "kullu_2023": {
                "name": "Kullu-Manali 2023 Torrential Surge (Beas River Surge)",
                "rainfall_rate_mm_hr": 95.0,
                "duration_hr": 3.5,
                "initial_soil_moisture": 0.42,
                "description": "Unprecedented monsoon cloudburst triggered 1,850 m³/s surge washing bridges, hotels, and NH-3."
            },
            "monsoon_beas": {
                "name": "Active Monsoon Riverbank Overflow Watch",
                "rainfall_rate_mm_hr": 50.0,
                "duration_hr": 10.0,
                "initial_soil_moisture": 0.38,
                "description": "Continuous multi-day rain in Kullu valley raising Beas water levels past warning stage at Bhuntar."
            },
            "normal_baseline": {
                "name": "Clear Weather Baseflow Regime",
                "rainfall_rate_mm_hr": 3.5,
                "duration_hr": 1.0,
                "initial_soil_moisture": 0.20,
                "description": "Typical calm alpine baseflow fed by seasonal snowmelt in upper Solang."
            }
        }
    },

    "teesta": {
        "id": "teesta",
        "name": "Teesta River Basin (North Sikkim Corridor)",
        "short_name": "Teesta (North Sikkim)",
        "district": "Mangan, Sikkim",
        "state": "Sikkim",
        "elevation_range": "650m - 5,200m",
        "dominant_geology": "Lingtse Gneiss, Daling Phyllites & Moraine Scree",
        "catchment_area_km2": 120.0,
        "base_flow_m3s": 50.0,
        "center_lat": 27.60,
        "center_lon": 88.58,
        "default_zoom": 10,
        "river_path": [
            [27.9800, 88.6200], # South Lhonak Glacial Lake
            [27.6000, 88.6400], # Chungthang Barrage / Dam
            [27.5000, 88.5300], # Mangan District HQ
            [27.4200, 88.5200], # Dikchu Hydro Project
            [27.2300, 88.5000], # Singtam Floodplain & Bridge
            [27.0800, 88.4700]  # Rangpo Border Reach
        ],
        "geotechnical": {
            "c_prime": 6800.0,
            "phi_prime_deg": 31.0,
            "gamma_sat": 19600.0,
            "gamma_w": 9810.0,
            "soil_depth_z": 1.9,
            "slope_beta_deg": 36.0,
            "k_sat_mm_hr": 16.5,
            "psi_suction_mm": 98.0,
            "theta_sat": 0.44,
            "theta_init_default": 0.24
        },
        "hydraulic": {
            "manning_n": 0.050,
            "bed_slope_s0": 0.027,
            "bottom_width_b": 26.0,
            "side_slope_z": 1.2
        },
        "settlements": [
            {
                "id": "chungthang",
                "name": "Chungthang Dam Township",
                "lat": 27.6000,
                "lon": 88.6400,
                "distance_km": 14.0,
                "elevation_m": 1650,
                "normal_depth_m": 2.5,
                "warning_depth_m": 5.0,
                "danger_depth_m": 6.8,
                "population": 2800,
                "priority": "CRITICAL"
            },
            {
                "id": "mangan",
                "name": "Mangan District HQ",
                "lat": 27.5000,
                "lon": 88.5300,
                "distance_km": 32.0,
                "elevation_m": 1180,
                "normal_depth_m": 3.2,
                "warning_depth_m": 6.2,
                "danger_depth_m": 8.2,
                "population": 4600,
                "priority": "HIGH"
            },
            {
                "id": "dikchu",
                "name": "Dikchu Hydro Station",
                "lat": 27.4200,
                "lon": 88.5200,
                "distance_km": 48.0,
                "elevation_m": 750,
                "normal_depth_m": 3.8,
                "warning_depth_m": 7.0,
                "danger_depth_m": 9.0,
                "population": 3100,
                "priority": "HIGH"
            },
            {
                "id": "singtam",
                "name": "Singtam Floodplain & Bridge",
                "lat": 27.2300,
                "lon": 88.5000,
                "distance_km": 68.0,
                "elevation_m": 420,
                "normal_depth_m": 4.5,
                "warning_depth_m": 8.0,
                "danger_depth_m": 10.2,
                "population": 14000,
                "priority": "STRATEGIC"
            }
        ],
        "authority": {
            "ddma_name": "Sikkim State Disaster Management Authority (SSDMA Mangan)",
            "siren_freq": "148.65 MHz VHF",
            "state_control": "State Emergency Operation Centre (Gangtok)",
            "local_dialects": "Nepali / Bhutia / Lepcha / English"
        },
        "scenarios": {
            "teesta_2023": {
                "name": "Teesta 2023 South Lhonak GLOF & Dam Washout",
                "rainfall_rate_mm_hr": 65.0,
                "duration_hr": 4.0,
                "initial_soil_moisture": 0.40,
                "description": "Glacial lake breach at South Lhonak washed out Chungthang HEP dam with 3,950 m³/s peak flash discharge."
            },
            "monsoon_teesta": {
                "name": "Active Monsoon Inundation Watch",
                "rainfall_rate_mm_hr": 55.0,
                "duration_hr": 8.0,
                "initial_soil_moisture": 0.38,
                "description": "Intense Eastern Himalayan orographic rainfall pushing river reaches above alert limits at Mangan and Dikchu."
            },
            "normal_baseline": {
                "name": "Clear Weather Baseflow Regime",
                "rainfall_rate_mm_hr": 4.0,
                "duration_hr": 1.0,
                "initial_soil_moisture": 0.22,
                "description": "Controlled post-monsoon baseflow through the Teesta valley hydroelectric cascade."
            }
        }
    },

    "chenab": {
        "id": "chenab",
        "name": "Chenab River Basin (Kishtwar & Machail Gorges)",
        "short_name": "Chenab (Kishtwar)",
        "district": "Kishtwar, Jammu & Kashmir",
        "state": "Jammu & Kashmir",
        "elevation_range": "950m - 4,600m",
        "dominant_geology": "Kishtwar Quartzites, Mica-Schist & Glacio-Fluvial Scree",
        "catchment_area_km2": 105.0,
        "base_flow_m3s": 42.0,
        "center_lat": 33.31,
        "center_lon": 75.76,
        "default_zoom": 10,
        "river_path": [
            [33.5600, 76.1200], # Machail Alpine Valley
            [33.4500, 75.9800], # Gulabgarh Confluence
            [33.3600, 75.8400], # Dul Hasti Dam Reach
            [33.3150, 75.7650], # Kishtwar Town Bridge
            [33.2400, 75.6800], # Thathri Rapid Corridor
            [33.1400, 75.5400]  # Doda City Riverbanks
        ],
        "geotechnical": {
            "c_prime": 8100.0,
            "phi_prime_deg": 33.0,
            "gamma_sat": 19500.0,
            "gamma_w": 9810.0,
            "soil_depth_z": 2.1,
            "slope_beta_deg": 37.0,
            "k_sat_mm_hr": 14.8,
            "psi_suction_mm": 112.0,
            "theta_sat": 0.43,
            "theta_init_default": 0.22
        },
        "hydraulic": {
            "manning_n": 0.047,
            "bed_slope_s0": 0.025,
            "bottom_width_b": 32.0,
            "side_slope_z": 1.25
        },
        "settlements": [
            {
                "id": "machail",
                "name": "Machail Base Camp (Bridge)",
                "lat": 33.5600,
                "lon": 76.1200,
                "distance_km": 6.0,
                "elevation_m": 2750,
                "normal_depth_m": 1.8,
                "warning_depth_m": 3.5,
                "danger_depth_m": 4.8,
                "population": 850,
                "priority": "CRITICAL"
            },
            {
                "id": "gulabgarh",
                "name": "Gulabgarh Confluence",
                "lat": 33.4500,
                "lon": 75.9800,
                "distance_km": 18.0,
                "elevation_m": 1850,
                "normal_depth_m": 2.6,
                "warning_depth_m": 4.8,
                "danger_depth_m": 6.2,
                "population": 2100,
                "priority": "HIGH"
            },
            {
                "id": "kishtwar_bridge",
                "name": "Kishtwar Town Bridge",
                "lat": 33.3150,
                "lon": 75.7650,
                "distance_km": 42.0,
                "elevation_m": 1250,
                "normal_depth_m": 3.5,
                "warning_depth_m": 6.8,
                "danger_depth_m": 8.8,
                "population": 16500,
                "priority": "STRATEGIC"
            },
            {
                "id": "doda_reach",
                "name": "Doda City Riverbank",
                "lat": 33.1400,
                "lon": 75.5400,
                "distance_km": 68.0,
                "elevation_m": 950,
                "normal_depth_m": 4.2,
                "warning_depth_m": 7.8,
                "danger_depth_m": 9.8,
                "population": 22000,
                "priority": "STRATEGIC"
            }
        ],
        "authority": {
            "ddma_name": "Kishtwar District Disaster Management Authority (DDMA)",
            "siren_freq": "149.20 MHz VHF",
            "state_control": "J&K Disaster Management Authority (JKDMA Jammu/Srinagar)",
            "local_dialects": "Kishtwari / Kashmiri / Hindi / Urdu"
        },
        "scenarios": {
            "kishtwar_2021": {
                "name": "Kishtwar 2021 Honzar Cloudburst Flash Surge",
                "rainfall_rate_mm_hr": 110.0,
                "duration_hr": 2.5,
                "initial_soil_moisture": 0.39,
                "description": "Violent high-altitude cloudburst generated torrential debris surge through Honzar gorge, destroying bridges."
            },
            "monsoon_chenab": {
                "name": "Active Monsoon Riverbank Overflow Watch",
                "rainfall_rate_mm_hr": 48.0,
                "duration_hr": 8.0,
                "initial_soil_moisture": 0.36,
                "description": "Persistent monsoon rains in Pir Panjal & Great Himalaya watersheds swelling Chenab gorge discharges."
            },
            "normal_baseline": {
                "name": "Clear Weather Baseflow Regime",
                "rainfall_rate_mm_hr": 3.8,
                "duration_hr": 1.0,
                "initial_soil_moisture": 0.20,
                "description": "Standard snowmelt baseflow passing through Dul Hasti hydroelectric reservoir."
            }
        }
    }
}

# Backward-compatible defaults pointing to Alaknanda / Chamoli basin
DEFAULT_REGION = HIMALAYAN_REGIONS["alaknanda"]
GEOTECHNICAL_PARAMS = DEFAULT_REGION["geotechnical"]
HYDRAULIC_PARAMS = DEFAULT_REGION["hydraulic"]
SETTLEMENTS = DEFAULT_REGION["settlements"]
SCENARIOS = DEFAULT_REGION["scenarios"]
