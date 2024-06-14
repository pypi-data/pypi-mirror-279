import os, json
import tiktoken
from .claim_extractor import ClaimExtractor
from .claim_verifier import ClaimVerifier

path_extracted_claim = "/data/yixiao/atomic_claims/unity_fine_tune_code_data/data/run_ft-ed_models_on_110_datapoints/three_new_models/model_generations/claim_extracted/gpt-4o.jsonl"
path_verification = '/data/yixiao/atomic_claims/unity_fine_tune_code_data/data/run_ft-ed_models_on_110_datapoints/three_new_models/model_generations/claim_verified/gpt-4o.jsonl'

output_path = './data/calculate_cost_claim_verification'
fp = open(output_path, 'w')
if __name__ == '__main__':
    model_name = 'gpt-4-0125-preview'
    # claim_extractor = ClaimExtractor(model_name, './data')'
    demon_dir = os.path.join('./data', 'demos')
    claim_verifier = ClaimVerifier(model_name=model_name, label_n=2,
                                   cache_dir='./data', demon_dir=demon_dir)
    total_data, total_tok = 0, 0
    with open(path_verification, "r") as f:
        data = [json.loads(line) for line in f.readlines() if line.strip()]
        for dict_item in data:
            if dict_item["abstained"] == True:
                fp.write(json.dumps(dict_item) + "\n")
                continue
            total_data += 1

            # response = dict_item["response"]
            # prompt_source = dict_item["prompt_source"]
            # model = dict_item["model"]
            # # sent_cnt = len(dict_item['fact_lst_lst'])
            # # all_claims_cnt = len(dict_item['all_facts_lst'])
            #
            # if "question" in dict_item and dict_item["question"]:
            #     question = dict_item["question"]
            #     snippet_lst, claim_list, all_claims, prompt_tok_cnt, response_tok_cnt = claim_extractor.qa_scanner_extractor(
            #         question, response,  cost_estimate_only=True)
            # else:
            #     question = ''
            #     snippet_lst, claim_list, all_claims, prompt_tok_cnt, response_tok_cnt = claim_extractor.non_qa_scanner_extractor(
            #         response, cost_estimate_only=True)
            #

            claim_search_results = dict_item["claim_search_results"]

            claim_verify_res_dict, prompt_tok_cnt, response_tok_cnt = claim_verifier.verifying_claim(
                claim_search_results, search_res_num=5, )

            total_tok += prompt_tok_cnt
            dict_item['prompt_method_input_tok_cnt'] = prompt_tok_cnt
            fp.write(json.dumps(dict_item) + "\n")

    print(f"total data: {total_data}, total token: {total_tok}")




