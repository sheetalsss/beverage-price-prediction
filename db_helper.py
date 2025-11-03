import pandas as pd
import joblib

# --- Load Model + Label Encoder ---
model = joblib.load("artifacts/model.pkl")
le = joblib.load("artifacts/label_encoder.pkl")

# --- Feature Columns (same as training) ---
model_features = [
    'income_levels', 'consume_frequency(weekly)', 'preferable_consumption_size',
    'health_concerns', 'age_group', 'cf_ab_score', 'zas_score',
    'gender_M', 'zone_2', 'zone_3', 'zone_4',
    'occupation_Retired', 'occupation_Student', 'occupation_Working Professional',
    'current_brand_Newcomer', 'awareness_of_other_brands_2', 'awareness_of_other_brands_3',
    'reasons_for_choosing_brands_Brand Reputation', 'reasons_for_choosing_brands_Price',
    'reasons_for_choosing_brands_Quality', 'flavor_preference_Traditional',
    'purchase_channel_Retail Store', 'packaging_preference_Premium', 'packaging_preference_Simple',
    'typical_consumption_situations_Casual (eg. At home)',
    'typical_consumption_situations_Social (eg. Parties)', 'bsi_1'
]

# --- Preprocessing Function ---
def process_data(
    gender, zone, occupation, income_levels, consumer_frequency,
    current_brand, preferable_consumption_size, awareness_of_other_brands,
    reasons_for_choosing_brands, flavor_preference, purchase_channel,
    packaging_preference, health_concerns, typical_consumption_situations, age_group
):
    # ✅ Label encoded mappings from training
    zone_map = {'Rural': 1, 'Semi-Urban': 2, 'Urban': 3, 'Metro': 4}
    income_map = {
        'Not Reported': 0, '<10L': 1, '10L - 15L': 2,
        '16L - 25L': 3, '26L - 35L': 4, '> 35L': 5
    }
    freq_map = {'0-2 times': 1, '3-4 times': 2, '5-7 times': 3}
    size_map = {'Small (250 ml)': 0, 'Large (1 L)': 1, 'Medium (500 ml)': 2}
    awareness_map = {'0 to 1': 1, '2 to 4': 2, 'above 4': 3}
    age_group_map = {'18-25': 0, '26-35': 1, '36-45': 2, '46-55': 3, '56-70': 4}
    health_map = {'Low': 0, 'Moderate': 1, 'High': 2}

    # Step 1 — Label Encoded / Numeric features
    input_data = {
        'income_levels': income_map.get(income_levels, 0),
        'consume_frequency(weekly)': freq_map.get(consumer_frequency, 0),
        'preferable_consumption_size': size_map.get(preferable_consumption_size, 0),
        'health_concerns': health_map.get(health_concerns, 0),
        'age_group': age_group_map.get(age_group, 0),
    }

    # Step 2 — One-hot encoded columns
    one_hot = {
        'gender_M': 1 if gender == 'M' else 0,
        'zone_2': 1 if zone_map.get(zone, 0) == 2 else 0,
        'zone_3': 1 if zone_map.get(zone, 0) == 3 else 0,
        'zone_4': 1 if zone_map.get(zone, 0) == 4 else 0,
        'occupation_Retired': 1 if occupation == 'Retired' else 0,
        'occupation_Student': 1 if occupation == 'Student' else 0,
        'occupation_Working Professional': 1 if occupation == 'Working Professional' else 0,
        'current_brand_Newcomer': 1 if current_brand == 'Newcomer' else 0,
        'awareness_of_other_brands_2': 1 if awareness_map.get(awareness_of_other_brands, 0) == 2 else 0,
        'awareness_of_other_brands_3': 1 if awareness_map.get(awareness_of_other_brands, 0) == 3 else 0,
        'reasons_for_choosing_brands_Brand Reputation': 1 if reasons_for_choosing_brands == 'Brand Reputation' else 0,
        'reasons_for_choosing_brands_Price': 1 if reasons_for_choosing_brands == 'Price' else 0,
        'reasons_for_choosing_brands_Quality': 1 if reasons_for_choosing_brands == 'Quality' else 0,
        'flavor_preference_Traditional': 1 if flavor_preference == 'Traditional' else 0,
        'purchase_channel_Retail Store': 1 if purchase_channel == 'Retail Store' else 0,
        'packaging_preference_Premium': 1 if packaging_preference == 'Premium' else 0,
        'packaging_preference_Simple': 1 if packaging_preference == 'Simple' else 0,
        'typical_consumption_situations_Casual (eg. At home)': 1 if typical_consumption_situations == 'Casual (eg. At home)' else 0,
        'typical_consumption_situations_Social (eg. Parties)': 1 if typical_consumption_situations == 'Social (eg. Parties)' else 0,
    }

    input_data.update(one_hot)

    # Step 3 — Derived scores
    zone_val = zone_map.get(zone, 1)
    aware_val = awareness_map.get(awareness_of_other_brands, 1)
    input_data['cf_ab_score'] = input_data['consume_frequency(weekly)'] / (1 + aware_val)
    input_data['zas_score'] = zone_val / (1 + input_data['income_levels'])
    input_data['bsi_1'] = 1 if current_brand == 'Established' and reasons_for_choosing_brands in ('Price', 'Quality') else 0

    # Step 4 — Build aligned DataFrame
    df = pd.DataFrame([input_data])
    df = df.reindex(columns=model_features, fill_value=0)
    return df


# --- Prediction Function ---
def predict(
    age,
    income_levels,
    health_concerns,
    consume_frequency,
    preferable_consumption_size,
    gender,
    zone,
    occupation,
    current_brand,
    awareness_of_other_brands,
    reasons_for_choosing_brands,
    flavor_preference,
    purchase_channel,
    packaging_preference,
    typical_consumption_situations
):
    # Convert age → age_group
    if age <= 25:
        age_group = '18-25'
    elif age <= 35:
        age_group = '26-35'
    elif age <= 45:
        age_group = '36-45'
    elif age <= 55:
        age_group = '46-55'
    else:
        age_group = '56-70'

    # Process and Predict
    input_encoded = process_data(
        gender, zone, occupation, income_levels, consume_frequency,
        current_brand, preferable_consumption_size, awareness_of_other_brands,
        reasons_for_choosing_brands, flavor_preference, purchase_channel,
        packaging_preference, health_concerns, typical_consumption_situations, age_group
    )

    pred = model.predict(input_encoded)
    pred_label = le.inverse_transform(pred.astype(int))[0]
    return pred_label


# --- Example Test ---
if __name__ == "__main__":
    print(predict(
        age=40,
        income_levels='> 35L',
        health_concerns='Low',
        consume_frequency='3-4 times',
        preferable_consumption_size='Medium (500 ml)',
        gender='M',
        zone='Urban',
        occupation='Working Professional',
        current_brand='Established',
        awareness_of_other_brands='above 4',
        reasons_for_choosing_brands='Brand Reputation',
        flavor_preference='Exotic',
        purchase_channel='Online',
        packaging_preference='Eco-Friendly',
        typical_consumption_situations='Active (eg. Sports, gym)'
    ))
