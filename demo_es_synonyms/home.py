import json

import streamlit as st
import pandas as pd

from demo_es_synonyms.es_client import EsClient
from demo_es_synonyms.footer import footer

es_client = EsClient()
available_synonyms = es_client.get_synonym_rules()['synonyms_set']
df_synonyms = pd.DataFrame(available_synonyms)


def remove_synonym_rule(rule_id):
    print("Remove synonym rule")
    es_client.delete_synonym_rule(rule_id)
    st.rerun()


def add_synonym_rule(rule_id, synonym):
    print("Add synonym rule")
    es_client.add_synonym_rule(rule_id, synonym)
    st.rerun()


st.set_page_config(page_title='Demo synonyms', page_icon='🧠', layout='wide')

col1, col2 = st.columns([1, 1])

with col1:
    st.write("## Search")
    search_query = st.text_input("Search query")
    if st.button("Search"):
        search_results = es_client.search_remark(search_query)
        print(search_results)
        processed_results = [
            {"score": hit["_score"], "remark": hit["_source"]["remarks"]}
            for hit in search_results["hits"]["hits"]
        ]
        st.dataframe(pd.DataFrame(processed_results), use_container_width=True)

with col2:
    st.write("## Synonym rules")
    my_table = st.dataframe(df_synonyms, on_select='rerun', selection_mode='multi-row', use_container_width=True)

    if st.button("Delete selected synonyms", key="synonym_delete_button"):
        for row_index in my_table.selection.rows:
            remove_synonym_rule(df_synonyms.loc[row_index, 'id'])
            st.rerun()

    st.write("### Add New Synonym Rule")
    with st.form("new_synonym_rule_form"):
        rule_id_input = st.text_input("Rule ID", key="rule_id")
        synonyms_input = st.text_input("Synonyms", key="synonyms")
        submit_button = st.form_submit_button("Add Synonym Rule")

    if submit_button:
        add_synonym_rule(rule_id_input, synonyms_input)
        st.rerun()


footer()