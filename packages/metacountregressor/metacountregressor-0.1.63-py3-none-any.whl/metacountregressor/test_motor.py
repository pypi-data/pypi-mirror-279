import pandas as pd
import numpy as np
import shap
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance

X, y = make_regression(n_samples=1000, n_features=100, n_informative=10, noise=0.1, random_state=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)


def shape_ply(df, y):
    df_features = df
    model = xgb.XGBRegressor(n_estimators=500, max_depth=20, learning_rate=0.1, subsample=0.8, random_state=33)
    model.fit(df_features, y)

    clustering = shap.utils.hclust(df_features, y)

    # PERMUATION fEATUre importance
    scoring = ['r2', 'neg_mean_squared_error']
    perm_importance = permutation_importance(model, df_features, y, scoring=scoring, n_repeats=5, random_state=33)
    perm_importance_r2 = pd.DataFrame(data={'importance': perm_importance['r2']['importances_mean']},
                                      index=df_features.columns)
    perm_importance_r2.sort_values(by='importance', ascending=False).plot(kind='bar')
    # plt.tight_layout()
    # plt.savefig('plot.png')
    # plt.show()

    print(1)

    # SHAPELY PART
    explainer = shap.Explainer(model)
    shap_values = explainer(df_features)
    # fig = shap.summary_plot(shap_values, df_features, show = False)

    # plt.figure(figsize=(10, 8))
    fig = shap.plots.beeswarm(shap_values, order=shap_values.abs.max(0), show=False)
    plt.gca().set_xticklabels([])
    plt.savefig('shap_values.png', bbox_inches='tight')
    plt.show()
    shap.plots.bar(shap_values.abs.mean(0), show=False)
    plt.gca().set_xticklabels([])
    plt.savefig('bar_values.png', bbox_inches='tight')

    shap.plots.bar(shap_values, clustering=clustering, clustering_cutoff=0.8, show=False)
    plt.gca().set_xticklabels([])
    plt.savefig('bar_valuesff.png', bbox_inches='tight')
    print(2)


def summary_stats(crash_data):
    # Calculate the count of crashes
    crash_observations = crash_data.shape[0]
    crash_factors = crash_data.shape[1]

    # Calculate the mean age of drivers involved in the crashes
    total_vehicle = crash_data['CASUALTY_TOTAL'].sum()

    # Calculate the median number of vehicles involved in the crashes
    median_vehicles = crash_data['CASUALTY_TOTAL'].median()

    # Calculate the mode of crash types
    mode_crash_type = crash_data['CASUALTY_TOTAL'].mode()[0]

    # Calculate the 25th and 75th percentiles of a numeric variable
    percentile_25 = crash_data['CASUALTY_TOTAL'].quantile(0.25)
    percentile_75 = crash_data['CASUALTY_TOTAL'].quantile(0.75)
    std_dev = crash_data['CASUALTY_TOTAL'].std()

    # Print the summary statistics
    print("Summary Statistics:")
    print('Total Crashes', total_vehicle)
    print("Crash Observation:", crash_observations)
    print("Crash Factors:", crash_factors)

    print("Median Vehicles Involved:", median_vehicles)
    print("Mode Crash Type:", mode_crash_type)

    print("Standard Deviation of Age:", std_dev)
    print("25th Percentile of Crash Totals:", percentile_25)
    print("75th Percentile of Crash Total:", percentile_75)

    latex_table = pd.DataFrame({
        'Statistic': ['Total Crashes', 'Crash Observation', 'Crash Factors', 'Median Vehicles Involved',
                      'Mode Crash Type', 'Standard Deviation of Age', '25th Percentile of Crash Totals',
                      '75th Percentile of Crash Total'],
        'Value': [total_vehicle, crash_observations, crash_factors, median_vehicles, mode_crash_type,
                  std_dev, percentile_25, percentile_75]
    }).to_latex(index=False)

    # Print the LaTeX table
    print(latex_table)
    summary_statsd = crash_data[
        ['CRASH_YEAR', 'CRASH_FIN_YEAR', 'CRASH_MONTH', 'CRASH_DAY_OF_WEEK', 'CRASH_HOUR']].describe()

    # Print the summary statistics
    print("Summary Statistics:")
    print(summary_statsd)

    if 'CRASH_SEVERITY' in crash_data:
        severity_counts = crash_data['CRASH_SEVERITY'].value_counts()
        print(severity_counts)


# Load data





# Convert data types

def clean_data_types(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            # Attempt to convert the column to numeric type
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df




# id folumn is a string drop
# feauture slection
def select_features(X_train, y_train, n_f=16):
    feature_names = X_train.columns
    # configure to select all features
    fs = SelectKBest(score_func=f_regression, k=16)

    # learn relationship from training data
    fs.fit(X_train, y_train)

    mask = fs.get_support()  # Boolean array of selected features
    selected_features = [feature for bool, feature in zip(mask, feature_names) if bool]
    # transform train input data
    X_train_fs = fs.transform(X_train)
    X_train_fs = pd.DataFrame(X_train_fs, columns=selected_features)
    X_train = X_train[selected_features]
    return X_train, fs


def findCorrelation(corr, cutoff=0.9, exact=None):
    """
    This function is the Python implementation of the R function
    `findCorrelation()`.

    Relies on numpy and pandas, so must have them pre-installed.

    It searches through a correlation matrix and returns a list of column names
    to remove to reduce pairwise correlations.

    For the documentation of the R function, see
    https://www.rdocumentation.org/packages/caret/topics/findCorrelation
    and for the source code of `findCorrelation()`, see
    https://github.com/topepo/caret/blob/master/pkg/caret/R/findCorrelation.R

    -----------------------------------------------------------------------------

    Parameters:
    -----------
    corr: pandas dataframe.
        A correlation matrix as a pandas dataframe.
    cutoff: float, default: 0.9.
        A numeric value for the pairwise absolute correlation cutoff
    exact: bool, default: None
        A boolean value that determines whether the average correlations be
        recomputed at each step
    -----------------------------------------------------------------------------
    Returns:
    --------
    list of column names
    -----------------------------------------------------------------------------
    Example:
    --------
    R1 = pd.DataFrame({
        'x1': [1.0, 0.86, 0.56, 0.32, 0.85],
        'x2': [0.86, 1.0, 0.01, 0.74, 0.32],
        'x3': [0.56, 0.01, 1.0, 0.65, 0.91],
        'x4': [0.32, 0.74, 0.65, 1.0, 0.36],
        'x5': [0.85, 0.32, 0.91, 0.36, 1.0]
    }, index=['x1', 'x2', 'x3', 'x4', 'x5'])

    findCorrelation(R1, cutoff=0.6, exact=False)  # ['x4', 'x5', 'x1', 'x3']
    findCorrelation(R1, cutoff=0.6, exact=True)   # ['x1', 'x5', 'x4']
    """

    def _findCorrelation_fast(corr, avg, cutoff):

        combsAboveCutoff = corr.where(lambda x: (np.tril(x) == 0) & (x > cutoff)).stack().index

        rowsToCheck = combsAboveCutoff.get_level_values(0)
        colsToCheck = combsAboveCutoff.get_level_values(1)

        msk = avg[colsToCheck] > avg[rowsToCheck].values
        deletecol = pd.unique(np.r_[colsToCheck[msk], rowsToCheck[~msk]]).tolist()

        return deletecol

    def _findCorrelation_exact(corr, avg, cutoff):

        x = corr.loc[(*[avg.sort_values(ascending=False).index] * 2,)]

        if (x.dtypes.values[:, None] == ['int64', 'int32', 'int16', 'int8']).any():
            x = x.astype(float)

        x.values[(*[np.arange(len(x))] * 2,)] = np.nan

        deletecol = []
        for ix, i in enumerate(x.columns[:-1]):
            for j in x.columns[ix + 1:]:
                if x.loc[i, j] > cutoff:
                    if x[i].mean() > x[j].mean():
                        deletecol.append(i)
                        x.loc[i] = x[i] = np.nan
                    else:
                        deletecol.append(j)
                        x.loc[j] = x[j] = np.nan
        return deletecol

    if not np.allclose(corr, corr.T) or any(corr.columns != corr.index):
        raise ValueError("correlation matrix is not symmetric.")

    acorr = corr.abs()
    avg = acorr.mean()

    if exact or exact is None and corr.shape[1] < 100:
        return _findCorrelation_exact(acorr, avg, cutoff)
    else:
        return _findCorrelation_fast(acorr, avg, cutoff)


# Normalize data



print('here is the main stuff')
NAH = 0
if NAH:
    df = pd.read_csv('rqc40516_MotorcycleQUT_engineer_crash.csv', skiprows=5)
    # Clean 'CRASH_SPEED_LIMIT' and convert to integer
    df['CRASH_SPEED_LIMIT'] = df['CRASH_SPEED_LIMIT'].str.replace(' km/h', '').astype(int)

    # Clean data types
    df = clean_data_types(df)

    # Encode categorical variables
    categories = ['CRASH_SEVERITY', 'CRASH_TYPE', 'CRASH_NATURE', 'CRASH_ATMOSPHERIC_CONDITION']
    df = pd.get_dummies(df, columns=categories)

    # Select only numeric columns
    numeric_types = ['int32', 'uint8', 'bool', 'int64', 'float64']
    df = df.select_dtypes(include=numeric_types)

    # Check for missing values and fill with column mean
    missing_values_count = df['CASUALTY_TOTAL'].isnull().sum()
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Remove unnecessary columns
    df.drop(columns=['CRASH_REF_NUMBER'], inplace=True)

    # Define columns to exclude from the analysis
    EXCLUDE = [
        'LONGITUDE', 'YEAR', 'DCA', 'ID', 'LATIT', 'NAME', 'SEVERITY',
        "CASUALTY", "CRASH_FIN_YEAR", "CRASH_HOUR"
    ]

    # Filter out excluded columns
    df = df[[col for col in df.columns if col not in EXCLUDE]]

    # Prepare target variable
    y = df['CASUALTY_TOTAL']

    # Check for finite values and compute correlations
    finite_check = df.apply(np.isfinite).all()
    df_clean = df.loc[:, finite_check]
    corr = df_clean.corr()

    # Identify and remove highly correlated features
    hc = findCorrelation(corr, cutoff=0.5)
    trimmed_df = df_clean.drop(columns=hc)

    # Feature selection
    df_cleaner, fs = select_features(trimmed_df, y)

"""
# Split data
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(df.drop('target_column', axis=1), df['target_column'],
                                                    test_size=0.2, random_state=42)
"""
