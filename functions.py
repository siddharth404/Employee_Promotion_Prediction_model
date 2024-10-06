# libraries
import numpy as np
import pandas as pd
import joblib


# getting only important features from inputs
def get_important_features(input_data):
    # unpacking input data
    employee_id, department, region, education = input_data[:4]
    gender, recruitment_channel, no_of_trainings, age = input_data[4:8]
    previous_year_rating, length_of_service, awards_won, avg_training_score = input_data[8:]

    # empty list of important features
    important_features = list()

    # defining important features for departments
    department_hr = 1 if department == "HR" else 0
    department_l = 1 if department == "legal" else 0
    department_sam = 1 if department == "Sales & Marketing" else 0
    department_t = 1 if department == "Technology" else 0
    important_features.extend([department_hr, department_l, department_sam, department_t])

    # defining important features for regions
    region_r3 = 1 if region == "region_3" else 0
    region_r4 = 1 if region == "region_4" else 0
    region_r5 = 1 if region == "region_5" else 0
    region_r6 = 1 if region == "region_6" else 0
    region_r7 = 1 if region == "region_7" else 0
    region_r9 = 1 if region == "region_9" else 0
    region_r11 = 1 if region == "region_11" else 0
    region_r12 = 1 if region == "region_12" else 0
    region_r17 = 1 if region == "region_17" else 0
    region_r18 = 1 if region == "region_18" else 0
    region_r19 = 1 if region == "region_19" else 0
    region_r20 = 1 if region == "region_20" else 0
    region_r21 = 1 if region == "region_21" else 0
    region_r22 = 1 if region == "region_22" else 0
    region_r23 = 1 if region == "region_23" else 0
    region_r24 = 1 if region == "region_24" else 0
    region_r25 = 1 if region == "region_25" else 0
    region_r26 = 1 if region == "region_26" else 0
    region_r28 = 1 if region == "region_28" else 0
    region_r29 = 1 if region == "region_29" else 0
    region_r31 = 1 if region == "region_31" else 0
    region_r32 = 1 if region == "region_32" else 0
    region_r33 = 1 if region == "region_33" else 0
    region_r34 = 1 if region == "region_34" else 0
    important_features.extend([region_r3, region_r4, region_r5, region_r6, region_r7, region_r9,
                               region_r11, region_r12, region_r17, region_r18, region_r19, region_r20,
                               region_r21, region_r22, region_r23, region_r24, region_r25, region_r26,
                               region_r28, region_r29, region_r31, region_r32, region_r33, region_r34])

    # defining important features for
    recruitment_channel_r = 1 if recruitment_channel == "referred" else 0
    important_features.extend([recruitment_channel_r])

    # extending other important features
    important_features.extend([previous_year_rating, length_of_service, avg_training_score])

    return important_features


# scale all important features within 0 to 1
def scale_features(important_features):
    # define dataframe to find max and min
    df_test = pd.read_csv('datasets/test.csv')

    # scale last 3 features
    important_features[-3] = (important_features[-3] - df_test['previous_year_rating'].min())/(df_test['previous_year_rating'].max() - df_test['previous_year_rating'].min())
    important_features[-2] = (important_features[-2] - df_test['length_of_service'].min())/(df_test['length_of_service'].max() - df_test['length_of_service'].min())
    important_features[-1] = (important_features[-1] - df_test['avg_training_score'].min())/(df_test['avg_training_score'].max() - df_test['avg_training_score'].min())

    return important_features


# make prediction using model
def model_predict(scaled_important_features):
    # loading model
    model = joblib.load('final_model.sav')

    # reshape the important features
    important_features = np.array(scaled_important_features).reshape(1, -1)

    return model.predict(important_features)


# create table of promotion percentage by column
def promotion_percentage(df, column):
    promotion_counts = df.groupby(column)['is_promoted'].value_counts(normalize=True).unstack()
    promotion_df = promotion_counts[1] * 100
    promotion_df = promotion_df.reset_index()
    promotion_df.columns = [column, 'percentage']
    return promotion_df


# create function with all 3 above functions
def input_data_to_prediction(input_data):
    important_features = get_important_features(input_data)
    scaled_features = scale_features(important_features)
    prediction = model_predict(scaled_features)
    return prediction[0]



