import streamlit as st

# Streamlit UI
st.title("Estimated Nutrition Needs Calculator")

def calculate_bmi(weight, height):
    if height == 0:
        return 0  # Prevent division by zero
    height_m = height / 100  # Convert height from cm to m
    bmi = weight / (height_m ** 2)
    return bmi

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    elif 30 <= bmi < 39.9:
        return "Obese"
    else:
        return "Morbidly Obese"

# Get user inputs
gender = st.selectbox("Select Gender", ["Male", "Female"])
weight = st.number_input("Enter weight (kg)", min_value=0.1, step=0.1)
height = st.number_input("Enter height (cm)", min_value=0.1, step=0.1)
activity_level = st.selectbox("Select Activity Level", ["RMR (1.0)", "Sedentary (1.2)", "Active (1.3)", "Very Active (1.4)"])
age = st.number_input("Enter age (years)", min_value=1, step=1)

# Validate height input
if height == 0:
    st.error("Height must be greater than 0 cm.")
else:
    # Calculate Mifflin-St Jeor RMR
    if gender == "Male":
        rmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        rmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    # Match the activity level selection correctly
    activity_factors = {
        "RMR (1.0)": 1.0,
        "Sedentary (1.2)": 1.2,
        "Active (1.3)": 1.3,
        "Very Active (1.4)": 1.4
    }
    activity_factor = activity_factors[activity_level]

    # Calculate Total Daily Energy Expenditure (TDEE)
    tdee = rmr * activity_factor
    st.write(f"**Estimated Daily Energy Expenditure:** {tdee:.2f} kcal/d (MSJ X AF)")

    # Calculate Macronutrient Needs
    protein_min = (0.15 * tdee) / 4  # 15% of calories from protein
    protein_max = (0.35 * tdee) / 4  # 35% of calories from protein
    protein_min = max(protein_min, 65)  # Ensure a minimum of 65g protein per day

    #st.write(f"**Recommended Protein Intake:** {protein_min:.1f}g - {protein_max:.1f}g per day")

    # Function to calculate Ideal Body Weight (IBW)
    def calculate_ibw(height, gender):
        height_in = height / 2.54  # Convert cm to inches
        if gender == "Male":
            return 50 + 2.3 * (height_in - 60)
        else:
            return 45.5 + 2.3 * (height_in - 60)
            
    ibw = calculate_ibw(height, gender)
    st.write(f"**Ideal Body Weight (IBW):** {ibw:.2f} kg (Devine Equation)")

    # Calculate and classify BMI
    bmi = calculate_bmi(weight, height)
    classification = classify_bmi(bmi)

    # Display the results
    st.write(f"**BMI:** {bmi:.2f}")
    st.write(f"**Classification:** {classification}")

    
    
    # List of disease states in alphabetical order
disease_states = [
    "ARDS (Acute Lung Injury)/ Ventilated", "Cancer", "Cerebral vascular disease", "Diabetes", 
    "Heart failure", "Liver", "Obese (non critical care)", 
    "Pancreatitis", "Renal", "Spinal Cord Injury", 
    "Trauma", "Wound healing"
]
st.header(f"Disease State Nutrition Needs Calculation")
# Streamlit dropdown (selectbox)
selected_disease = st.selectbox("Select Disease State", disease_states)

# Conditional logic for each disease state
if selected_disease == "ARDS (Acute Lung Injury)/ Ventilated":
    # --- Energy Needs Calculation ---
    st.subheader("ARDS (Acute Lung Injury)/ Ventilated Nutrient Needs")
    if bmi < 30:
        # Non-obese patient: Use Penn State Equation
        st.subheader(f"Non-Obese Patient - Penn State Equation")
        minute_vent = st.number_input(f"Enter Minute Ventilation (L/min)", min_value=0.0, step=0.1, key="mv_nonobese")
        max_temp = st.number_input(f"Enter Max Temperature in past 24 hrs (°C)", min_value=0.0, step=0.1, key="temp_nonobese")
        
        # Penn State Equation for non-obese:
        # TDEE = (0.96 * RMR) + (31 * Minute Ventilation) + (167 * Max Temp) - 6212
        tdee = (0.96 * rmr) + (31 * minute_vent) + (167 * max_temp) - 6212
        st.write(f"**Estimated Total Daily Energy Expenditure (TDEE):** {tdee:.0f} kcal/day")
        
    elif bmi < 50:
        # Obese patient (BMI = 30-50)
        st.subheader("Obese Patient")
        if age < 60: 
            st.write(f"For obese patients under 60, use ASPEN guidelines (11-14 kcal/kg of actual body weight BMI 30-50).")
            tdee_low = 11 * weight
            tdee_high = 14 * weight
            st.write(f"**Estimated Energy Needs:** {tdee_low:.0f} - {tdee_high:.0f} kcal/day")
        else:
            st.write(f"For obese patients over 60, use the Modified Penn State Equation.")
            minute_vent = st.number_input("Enter Minute Ventilation (L/min) for Modified Penn State", min_value=0.0, step=0.1, key="mv_obese")
            max_temp = st.number_input("Enter Max Temperature in past 24 hrs (°C) for Modified Penn State", min_value=0.0, step=0.1, key="temp_obese")            
            # Modified Penn State Equation for obese patients over 60:
            # TDEE = (0.71 * RMR) + (64 * Minute Ventilation) + (85 * Max Temp) - 3085
            tdee = (0.71 * rmr) + (64 * minute_vent) + (85 * max_temp) - 3085
            st.write(f"**Estimated Total Daily Energy Expenditure (TDEE):** {tdee:.0f} kcal/day")
    
    else:
        if age < 60: 
            st.write("For obese patients with BMI >50 who are under 60, use ASPEN guidelines (22-25 kcal/kg of actual body weight BMI 30-50).")
            tdee_low = 22 * weight
            tdee_high = 25 * weight
            st.write(f"**Estimated Energy Needs:** {tdee_low:.0f} - {tdee_high:.0f} kcal/day")
        else:
            st.write("For obese patients over 60, use the Modified Penn State Equation.")
            minute_vent = st.number_input("Enter Minute Ventilation (L/min) for Modified Penn State", min_value=0.0, step=0.1, key="mv_obese")
            max_temp = st.number_input("Enter Max Temperature in past 24 hrs (°C) for Modified Penn State", min_value=0.0, step=0.1, key="temp_obese")            
            # Modified Penn State Equation for obese patients over 60:
            # TDEE = (0.71 * RMR) + (64 * Minute Ventilation) + (85 * Max Temp) - 3085
            tdee = (0.71 * rmr) + (64 * minute_vent) + (85 * max_temp) - 3085
            st.write(f"**Estimated Total Daily Energy Expenditure (TDEE):** {tdee:.0f} kcal/day")
    
    # Protein Needs Calculation
    st.write(f"**Estimated Protein Needs:**")
    
    if 30 <= bmi < 39.9:
        protein_needs = 2 * ibw
        st.write(f"{protein_needs:.0f} g/d (2g/kg IBW)") 
    elif bmi >= 40:
        protein_needs = (2.2 * ibw, 2.5 * ibw)
        st.write(f"{protein_needs[0]:.0f} - {protein_needs[1]:.0f} g/d (2.2-2.5g/kg IBW)")
    else:
        protein_low = 1.2 * weight
        protein_high = 1.5 * weight
        st.write(f"{protein_low:.0f} - {protein_high:.0f} g/d (1.2-1.5 g/kg actual weight)") 

elif selected_disease == "Cancer":
    st.subheader("Cancer Nutrition Recommendations")

    # Energy Needs
    if bmi < 30:  # Non-obese
        kcal_low = 25 * weight
        kcal_high = 30 * weight
        kcal_hyper_low = 30 * weight
        kcal_hyper_high = 35 * weight
        kcal_stressed = 35 * weight
        st.write(f"""
        **Energy Needs (Non-Obese):**  
        - {kcal_low:.0f} to {kcal_high:.0f} kcal/day for non-ambulatory or sedentary adults  
        - {kcal_hyper_low:.0f} to {kcal_hyper_high:.0f} kcal/day for hypermetabolic patients, for weight gain, during the first month after HSCT, or for an anabolic patient  
        - {kcal_stressed:.0f} kcal/day and above for hypermetabolic or severely stressed patients, patients with acute GVHD, during head and neck chemoradiation, or for those with malabsorption  
        """)
    else:  # Obese
        st.write("""
        **Energy Needs (Obese):**  
        - Needs are widely variable. Use clinical judgment, especially for the obese patient.  
        """)

    # Protein Needs
    protein_low = 1.0 * weight
    protein_high = 1.2 * weight
    protein_treatment_low = 1.2 * weight
    protein_treatment_high = 1.5 * weight
    protein_transplant_low = 1.5 * weight
    protein_transplant_high = 2.0 * weight
    protein_increased_low = 1.5 * weight
    protein_increased_high = 2.5 * weight

    st.write(f"""
    **Protein Needs:**  
    - {protein_low:.1f} to {protein_high:.1f} g/day for non-stressed patient with cancer  
    - {protein_treatment_low:.1f} to {protein_treatment_high:.1f} g/day for patients undergoing treatment  
    - {protein_transplant_low:.1f} to {protein_transplant_high:.1f} g/day for stem cell transplant  
    - {protein_increased_low:.1f} to {protein_increased_high:.1f} g/day for increased protein needs such as protein-losing enteropathies or wasting  
    """)

elif selected_disease == "Cerebral vascular disease":
    st.subheader("Cerebral Vascular Disease Nutrition Recommendations")

    # Energy Needs
    kcal_needs = rmr * 1.3
    st.write(f"""
    **Energy Needs:**  
    - {kcal_needs:.0f} kcal/day for sedentary individuals (RMR x 1.3 activity factor)  
    - Higher needs if more active  
    """)

    # Protein Needs
    protein_low = 0.8 * weight
    protein_high = 1.0 * weight
    st.write(f"""
    **Protein Needs:**  
    - {protein_low:.1f} to {protein_high:.1f} g/day unless modified for a subsequent condition  
    """)

    # Fluid Needs
    fluid_low = 25 * weight
    fluid_high = 35 * weight
    st.write(f"""
    **Fluid Needs:**  
    - {fluid_low:.0f} to {fluid_high:.0f} ml/day; emphasize non-energy containing fluids  
    """)

    # Macronutrient Distribution
    st.write("""
    **Macronutrient Distribution:**  
    - Carbohydrates: 50-60% of total daily energy  
    - Total Fat: 25-35% of total daily energy  
    - Saturated & Trans-fat: Less than 7%  
    """)

    # Sodium Recommendations
    st.write("""
    **Sodium Recommendations:**  
    - 2-4 gm/day for individuals with hypertension  
    - Overall heart-healthy diet recommendations  
    """)

elif selected_disease == "Diabetes":
    st.subheader("Diabetes Nutrition Recommendations")

    # Energy Needs
    if bmi < 25:  # Normal weight
        kcal_low = 25 * weight
        kcal_high = 30 * weight
        st.write(f"""
        **Energy Needs:**  
        - {kcal_low:.0f} to {kcal_high:.0f} kcal/day for normal weight  
        """)
        # Carbohydrate Recommendations
        g_carb_low = (kcal_low * 0.4)/4
        g_carb_high = (kcal_high * 0.45)/4
        st.write(f"""
        **Carbohydrate Needs:**  
        - grams CHO: {g_carb_low:.0f} g - {g_carb_high:.0f} g (40-45% of total energy needs) 
        - Base ideal percentage of kcal from CHO, protein, and fat on individual assessment & plan  
        """)
    elif bmi >= 25 and bmi < 30:  # Overweight
        kcal_needs = rmr * activity_factor
        st.write(f"""
        **Energy Needs:**  
        - {kcal_needs:.0f} kcal/day for overweight (Mifflin-St Jeor x activity factor)  
        """)
        # Carbohydrate Recommendations
        g_carb_low = (kcal_needs * 0.4)/4
        g_carb_high = (kcal_needs * 0.45)/4
        st.write(f"""
        **Carbohydrate Needs:**  
        - grams CHO: {g_carb_low:.0f} g - {g_carb_high:.0f} g (40-45% of total energy needs) 
        - Base ideal percentage of kcal from CHO, protein, and fat on individual assessment & plan  
        """)
    else:  # Obese or very inactive
        kcal_needs = 20 * weight
        st.write(f"""
        **Energy Needs:**  
        - {kcal_needs:.0f} kcal/day for obese or very inactive  
        """)
        # Carbohydrate Recommendations
        g_carb_low = (kcal_needs * 0.4)/4
        g_carb_high = (kcal_needs * 0.45)/4
        st.write(f"""
        **Carbohydrate Needs:**  
        - grams CHO: {g_carb_low:.0f} g - {g_carb_high:.0f} g (40-45% of total energy needs) 
        - Base ideal percentage of kcal from CHO, protein, and fat on individual assessment & plan  
        """)

    # Protein Needs
    protein_low = 0.8 * weight
    protein_high = 1.0 * weight
    protein_repletion_low = 1.0 * weight
    protein_repletion_high = 1.5 * weight
    st.write(f"""
    **Protein Needs:**  
    - {protein_low:.1f} to {protein_high:.1f} g/day for maintenance  
    - {protein_repletion_low:.1f} to {protein_repletion_high:.1f} g/day for repletion needs  
    - Advise 15-20% of daily calories from protein  
    """)

    # Fiber Recommendations
    if gender == "Male":
        fiber_needs = 38
    else:
        fiber_needs = 25
    st.write(f"""
    **Fiber Needs:**  
    - General recommendation: {fiber_needs} g/day  
    - DRI = 14 g/1000 kcal  
    """)

    # Fluid Needs
    fluid_low = 25 * weight
    fluid_high = 35 * weight
    st.write(f"""
    **Fluid Needs:**  
    - {fluid_low:.0f} to {fluid_high:.0f} ml/day  (25-35 ml/kg)
    """)

elif selected_disease == "Heart failure":
    st.subheader("Heart Failure Nutrition Recommendations")

    # Energy Needs using Mifflin or Harris Benedict formula
    kcal_needs = rmr * activity_factor
    st.write(f"""
    **Energy Needs:**   
    - Estimated kcal/day: {kcal_needs:.0f} kcal/day (Mifflin-St Jeor or Harris-Benedict formula x activity factor for energy needs) 
    """)

    # Protein Needs
    protein_low = 1.1 * weight
    protein_high = 1.4 * weight
    st.write(f"""
    **Protein Needs:**  
    - {protein_low:.1f} to {protein_high:.1f} g/day for protein intake (1.1 - 1.4 g/kg) 
    """)

    # Sodium Needs
    sodium_restriction = "<2000 mg Na/day"
    st.write(f"""
    **Sodium Needs:**  
    - Restrict sodium to {sodium_restriction}  
    """)

    # Fluid Needs
    fluid_low = 1.4
    fluid_high = 1.9
    # Adjust based on serum sodium
    if bmi < 25:  # Normal weight assumption
        fluid_recommendation = f"1.4-1.9 L/day depending on clinical symptoms; <2L/day for serum sodium <130mEq/L"
    else:  # For obese or very inactive
        fluid_recommendation = f"1.4-1.9 L/day depending on clinical symptoms; <2L/day for serum sodium <130mEq/L"
    
    st.write(f"""
    **Fluid Needs:**  
    - {fluid_low} to {fluid_high} L/day depending on clinical symptoms   
    - <2L/day for serum sodium <130mEq/L  
    """)

elif selected_disease == "Liver":
    st.subheader("Liver Disease Nutrition Recommendations")

    # Energy Needs for Liver Disease
    kcal_needs = 25 * weight  # Base energy needs
    kcal_high = 30 * weight   # Higher range
    kcal_range = f"{kcal_needs:.0f} to {kcal_high:.0f} kcal/day"
    st.write(f"""
    **Energy Needs:**  
    - {kcal_range} (25-30 kcal/kg)
    """)

    # Protein Needs for Liver Disease
    protein_low = 1 * weight
    protein_high = 1.5 * weight
    st.write(f"""
    **Protein Needs:**   
    - {protein_low:.1f} to {protein_high:.1f} g/day (1 to 1.5 g/kg body weight)
    """)

    # Hepatic Encephalopathy Consideration
    st.write(f"""
    **Hepatic Encephalopathy:**  
    - No need to restrict protein in Hepatic Encephalopathy as recent studies do not support this.  
    - Hepatic Encephalopathy should be treated with FDA-approved medications (e.g., lactulose).
    """)

elif selected_disease == "Obese (non critical care)":
    st.subheader("Obese (Non-Critical Care) Nutrition Recommendations")

    # Energy Needs
    st.write(f"""
    **Energy Needs (TDEE):**  
    - Mifflin-St. Jeor equation to estimate RMR  
    - Multiplied by an activity factor of {activity_factor} for {activity_level} individuals  
    - Total daily energy expenditure (TDEE): {tdee:.0f} kcal/day
    """)

    # Protein Needs
    st.write(f"""
    **Protein Needs:**  
    - Individualized to provide 15% to 35% of energy as protein.  
    - Estimated protein intake: {protein_min:.1f} to {protein_max:.1f} grams/day  
    - Minimum of 65-70 grams protein/day
    """)

elif selected_disease == "Pancreatitis":
    energy = 25 * weight  # 25 kcal/kg for Pancreatitis
    protein = 1.5 * weight  # 1.5 g/kg of protein for Pancreatitis

    st.subheader("Pancreatitis Nutrition Recommendations")

    # Energy Needs
    st.write(f"**Energy Needs:** 25 kcal/kg of weight, total energy requirement: {energy:.0f} kcal/day")

    # Protein Needs
    st.write(f"**Protein Needs:** 1.5 g/kg of weight, total protein requirement: {protein:.1f} g/day")

    # Feeding Recommendations
    st.write("""
    **Feeding Recommendations:**
    - **Jejunal Feeding** (below ligament of Treitz) recommended if there is feeding intolerance.
    - **Elemental enteral formula** is recommended for patients with feeding intolerance.
    """)

elif selected_disease == "Renal":
    # Energy needs for ARF
    energy_low = 25 * weight  # 25 kcal/kg for ARF
    energy_high = 35 * weight  # 35 kcal/kg for ARF
    st.subheader("Renal Disease (ARF) Nutrition Recommendations")
    st.write(f"**Energy Needs (ARF):** 25-35 kcal/kg of weight")
    st.write(f"Total energy requirement range: {energy_low:.0f} - {energy_high:.0f} kcal/day")

    # Protein needs for different renal conditions
    protein = 0.8 * weight  # Default protein for AKI without dialysis
    st.write("**Protein Needs (AKI):**")
    st.write(f"Without dialysis: {protein:.1f} g/day (0.8 g/kg)")

    # Adjust protein for different conditions
    st.write(f"""**Protein Needs:**  
    - Renal Replacement Therapy: {weight * 1.2:.0f} g - {weight * 1.5:.0f} g (1.2-1.5 g/kg)
    - AKI: {weight * 0.8:.0f} g - {weight * 1.0:.0f} g (0.8-1.0 g/kg without dialysis); {weight * 1.2:.0f} g - {weight * 1.5:.0f} g (1.2-1.5 g/kg with initiation of RRT)  
    - PD/HD: {weight * 1.2:.0f} g - {weight * 1.3:.0f} g (1.2-1.3 g/kg PD), up to {weight * 1.5:.0f} g - {weight * 1.8:.0f} g (1.5-1.8 g/kg HD) 
    - CRRT: up to {weight * 2.5 :.0f} g (2.5 g/kg)  

    **Fluid Recommendations:**  
    - Predialysis, PD, CRRT: as tolerated  
    - HD: 500 ml + urine output, anuric (<75 ml/day): 1-1.2 L/day  
    """)
    
    # Fluid needs
    st.write("**Fluid Needs:**")
    st.write("""
    - **Predialysis, PD, CRRT:** As tolerated
    - **HD (Hemodialysis):** 500 ml + urine output, if anuric (<75 ml/day) fluid requirement is 1-1.2L/day
    """)

elif selected_disease == "Spinal Cord Injury":
    # Energy needs for Quadriplegic and Paraplegic
    if weight > 0:
        # Energy calculation based on SCI type
        if st.selectbox("Select SCI type", ["Quadriplegic", "Paraplegic"]) == "Quadriplegic":
            energy = 20 * weight  # 20-23 kcal/kg for Quadriplegic
            energy_high = 23 * weight  # 23 kcal/kg upper range for Quadriplegic
            st.write(f"**Energy Needs Quadriplegic:** {energy:.0f} - {energy_high:.0f} kcal/day (20-23 kcal/kg)")
        else:
            energy = 27 * weight  # 27 kcal/kg for Paraplegic
            st.write(f"**Energy Needs Paraplegic:** {energy:.0f} kcal/day (27 kcal/kg)")

    # Protein needs for SCI
    st.write("**Protein Requirements:**")
    st.write(f"""
    - **Immediately following SCI (Acute Phase):** {1.5 * weight:.0f} - {2.0 * weight:.0f} (1.5-2.0 g/kg)
    - **Long term (Chronic Phase):** {0.8 * weight:.0f} - {1 * weight:.0f} (0.8-1.0 g/kg)
    """)

    # Consideration for skin breakdown
    st.write("""
    **Considerations:**
    - Investigate for **skin breakdown** and provide appropriate interventions, especially in the acute phase.
    """)

elif selected_disease == "Trauma":
    # Energy needs for Trauma
    if weight > 0:
        # Energy calculation based on intubated or non-intubated status
        if st.selectbox("Is the patient intubated?", ["Yes", "No"]) == "Yes":
            energy = 20 * weight  # 20-25 kcal/kg for intubated patients
            energy_high = 25 * weight
            st.write(f"**Energy Needs (Intubated):** 20-25 kcal/kg")
            st.write(f"Total energy requirement range: {energy:.0f} - {energy_high:.0f} kcal/day")
        else:
            energy = 25 * weight  # 25-35 kcal/kg for non-intubated patients
            energy_high = 35 * weight
            st.write(f"**Energy Needs (Non-Intubated):** 25-35 kcal/kg")
            st.write(f"Total energy requirement range: {energy:.0f} - {energy_high:.0f} kcal/day")

    # Protein needs for Trauma
    st.write("**Protein Requirements for Trauma:**")
    st.write("""
    - **1.5-2.0 g/kg** of body weight.
    """)
    
    # Vitamin supplementation
    st.write("**Vitamin Supplementation for Trauma Recovery:**")
    st.write("""
    - **Vitamin C:** 1000 mg x 7 days
    - **Vitamin E:** 1000 IU x 7 days
    - **Selenium:** 200 mcg x 7 days
    """)

    # TBI (Traumatic Brain Injury) consideration
    st.write("**Traumatic Brain Injury (TBI) Considerations:**")
    st.write("""
    - Energy needs: **120-160%** of basal energy needs
    - Protein needs: **1.5-2.0 g/kg** of body weight
    """)
    
    # Tube feeding phase
    st.write("""
    **Tube Feeding Phase (Day 1 to Day 7):**
    - Aim to provide nutrition via tube feeding and gradually transition to standard feeding after 7 days.
    """)

elif selected_disease == "Ventilated":
    if weight > 0 and height > 0:
        st.write(f"**Energy Requirements for Ventilated Patient:**")
        
        if bmi >= 30 and bmi <= 50:
            energy_low = 11 * weight  # 11-14 kcal/kg for BMI 30-50
            energy_high = 14 * weight
            st.write(f"**BMI 30-50:** Energy needs range from {energy_low:.0f} - {energy_high:.0f} kcal/day (based on actual BW)")

        elif bmi > 50:
            # For BMI > 50, use IBW for energy calculation
            ideal_bw = 22 * (height - 100)  # Simplified formula for Ideal Body Weight (IBW)
            energy_low = 22 * ideal_bw
            energy_high = 25 * ideal_bw
            st.write(f"**BMI > 50:** Energy needs range from {energy_low:.0f} - {energy_high:.0f} kcal/day (based on IBW)")
        
        # Protein Requirements
        st.write("**Protein Requirements for Ventilated Patients:**")
        if bmi >= 30 and bmi <= 40:
            protein = 2 * weight  # 2g/kg IBW for BMI 30-40
            st.write(f"**BMI 30-40:** Protein needs: {protein:.0f} g/day based on IBW")
        elif bmi > 40:
            protein = 2.5 * weight  # 2-2.5g/kg IBW for BMI >40
            st.write(f"**BMI >40:** Protein needs: {protein:.0f} g/day based on IBW")

        # Parenteral Nutrition (PN)
        st.write("""
        **Parenteral Nutrition (PN):**
        - Start with **80%** of estimated energy needs initially.
        - Gradually increase to goal as the patient stabilizes.
        """)

        # Additional Recommendations
        st.write("""
        **Additional Recommendations:**
        - **24-hour urine for Nitrogen (N2) balance** suggested for further nutritional monitoring.
        """)

elif selected_disease == "Wound healing":
    if weight > 0:
        st.write(f"**Energy Requirements for Wound Healing:**")
        
        # Energy needs based on weight
        energy_low = 30 * weight
        energy_high = 35 * weight
        st.write(f"Energy needs: {energy_low:.0f} - {energy_high:.0f} kcal/day")

        # Additional energy for underweight/losing weight
        if bmi < 18.5:  # Underweight or losing weight
            energy_underweight_low = 35 * weight
            energy_underweight_high = 40 * weight
            st.write(f"For underweight/losing weight: Energy needs increase to {energy_underweight_low:.0f} - {energy_underweight_high:.0f} kcal/day")
        
        # Protein Requirements
        st.write("**Protein Requirements for Wound Healing:**")
        protein_low = 1.25 * weight
        protein_high = 1.5 * weight
        st.write(f"Protein needs: {protein_low:.0f} - {protein_high:.0f} g/day (1.25-1.5 g/d)")

        # Fluid Requirements
        st.write("**Fluid Requirements for Wound Healing:**")
        fluid_min = 30 * weight
        fluid_max = 40 * weight
        st.write(f"""
        - Fluid needs: {fluid_min:.0f} - {fluid_max:.0f} ml/day (>30 ml/kg with minimum 1500 mL unless medical limitations such as cardiac or renal dise)
        - Stage III-IV Wounds or Fluid Losses: {fluid_min:.0f} - {fluid_max:.0f} (30 - 40 ml/kg, consider fluid losses from draining wounds, fever, stool/ostomy output, etc.
        """)

        # Vitamin and Mineral Supplements
        st.write("""
        **Supplementation:**
        - Offer **vitamin and mineral supplements** when dietary intake is poor or deficiencies are confirmed or suspected.
        - Provide **enhanced foods and/or oral supplements** between meals if needed.
        - Encourage consumption of a balanced diet that includes good sources of vitamins and minerals.
        """)

#General Fluid Needs
st.title("General Fluid Requirements (AND)")

if 14 <= age <= 55:
    st.write(f""" 
    - Average Healthy Adult: {30 * weight} - {35 * weight} ml (30-35 ml/kg) """)
elif 55 < age <= 65:
    st.write(f""" 
    - Adults 55-65 years: {30 * weight} ml (30 ml/kg) """)
elif age > 65:
    st.write(f""" 
    - Adults > 65 years: {25 * weight} ml (25 ml/kg) """) 
else:
    st.write(f"""
    **Holiday-Segar Method (commonly used for peds):**
    
    - 100ml/kg up to 1000ml + 50ml/kg for each kg > 10.
    
    - Or 1500 ml + 20ml/kg for each kg > 20.
    """)

# Function to calculate corrected calcium
def calculate_corrected_calcium(serum_ca, albumin):
    return serum_ca + 0.8 * (4 - albumin)

# Streamlit UI
st.title("Corrected Calcium Calculator")

# User inputs
serum_ca = st.number_input("Enter Serum Calcium (mg/dL)", min_value=0.0, step=0.1)
albumin = st.number_input("Enter Albumin (g/dL)", min_value=0.0, step=0.1)

# Calculation and display result
if serum_ca and albumin:
    corrected_ca = calculate_corrected_calcium(serum_ca, albumin)
    st.write(f"**Corrected Calcium:** {corrected_ca:.2f} mg/dL")
else:
    st.write("Please enter valid values for Serum Calcium and Albumin.")

st.write(f"""

***This page was created by Leah Newmark, RD, CNSC and Machine Learning Engineer***""")
