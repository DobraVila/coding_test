from flask import Flask, render_template, jsonify, request
import pandas as pd

app = Flask(__name__) # instance of a flask

# define the pages
@app.route('/') # sends us to default page otherwise specify page where you want to go by adding /home_page etc
def home_page(): # define what is going to be displayed
    return render_template('index.html')

# df for section A
df_1 = pd.read_csv('datasets/9606_abund.txt', delimiter='\t', header = 0)
df_1['Mean-copy-number'] = pd.to_numeric(df_1['Mean-copy-number'], errors='coerce')

# df for section B
df_2 = pd.read_csv('datasets/9606_gn_dom.txt', delimiter='\t', header = 0)
df_2['Eval'] = pd.to_numeric(df_2['Eval'], errors='coerce')

#Section_A_result
#Section_A_1
@app.route('/count-rows')
def count_copy_number():
    rm_duplicated_rows = df_1.drop_duplicates(subset=['Ensembl_protein', 'Mean-copy-number'])
    row_count = rm_duplicated_rows.shape[0]
    return jsonify(row_count=row_count) #requires a key-value format to serialize data into JSON

#Section_A_2
@app.route('/compute_stats')
def m_sd():
    stats = df_1.groupby('Ensembl_protein')['Mean-copy-number'].agg(['mean', 'std']).reset_index() #resets indecies
    stats.rename(columns={'Ensembl_protein':'Ensembl protein','mean':'M', 'std':'SD'}, inplace=True) #modifies df directly
    a_2_table = stats.to_html(index=False, classes="table table-bordered", border=0, float_format="%.2f")
    return jsonify(stats_table=a_2_table)

#Section_A_3"
@app.route('/percentile_rank')
def percentile_rank():
    stats = df_1.groupby('Ensembl_protein')['Mean-copy-number'].agg(['mean', 'std']).reset_index()
    stats.rename(columns={'Ensembl_protein': 'Ensembl protein', 'mean': 'M', 'std': 'SD'}, inplace=True)

    # Calculate percentile rank
    total_values = len(stats)
    stats['Percentile Rank'] = (stats['M'].rank(ascending=False, method='min') / total_values) * 100

    ## added so the table is more user-friendly
    sort_order = request.args.get('order', 'desc')
    if sort_order == 'asc':
        rank_df = stats[['Ensembl protein', 'M', 'Percentile Rank']].sort_values('Percentile Rank', ascending=True)
    elif sort_order == 'desc':
        rank_df = stats[['Ensembl protein', 'M', 'Percentile Rank']].sort_values('Percentile Rank', ascending=False)
    final_df = rank_df.to_html(index=False, classes="table table-bordered", border=0, float_format="%.2f")
    return jsonify(rank_table=final_df)

#Section_B_1
@app.route('/max_avg_abundance')
def max_abundance():
    max_domain = (
        df_2.groupby('Domain')['Eval']
        .mean()
        .reset_index()
        .nlargest(1, 'Eval')
        .iloc[0]
    )
    df_2_domain = max_domain['Domain']
    df_2_eval = max_domain['Eval']

    #output returned as JSON
    return jsonify({'domain': df_2_domain, 'eval': round(df_2_eval, 6)})

#Section B2
@app.route('/stats_percentile')
def stats_percentile():
    df_merged = pd.merge(df_1,df_2, on='Gn', how = 'inner')

    converted_data = df_merged.groupby('Domain')['Mean-copy-number'].agg(['mean', 'std']).reset_index() #resets indecies
    converted_data.rename(columns={'mean':'M', 'std':'SD'}, inplace=True) #modifies df directly
    converted_data['Percentile Rank'] = (converted_data['M'].rank(ascending=True, method='min') / len(converted_data)) * 100

    b_2_1_table = converted_data[['Domain', 'M', 'SD']].to_html(index=False, classes="table table-bordered", border=0, float_format="%.2f")
    b_2_2_table = converted_data[['Domain', 'Percentile Rank']].to_html(index=False, classes="table table-bordered", border=0, float_format="%.2f")
    return jsonify(table_2_1 = b_2_1_table, table_2_2 = b_2_2_table)

# run the app
if __name__ == '__main__':
    app.run()
