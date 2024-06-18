from fairbalance.metrics import FairnessAnalysis


class methodSelection:

    def find_best_method(self, X, y, positive_output, protected_attributes, privileged_classes):

        # Idea : evaluate balance for each protected attribute, from that
        # decide what mitigation to apply for each protected attribute,
        # the decide which processor (how??)

        FA = FairnessAnalysis(X, y, positive_output,
                              protected_attributes, privileged_classes)
        FA.get_fairness_analysis()

        initial_balance = {}

        for protected_attribute in protected_attributes:
            RMSDIR = FA.RMSDIR[protected_attribute]
            RMSPMI = FA.RMSPMI[protected_attribute]
            balance_index = FA.balance_index[protected_attribute]
            CBS = FA.attribute_balance_score[protected_attribute]

            initial_balance[protected_attribute] = {
                "RMSDIR": RMSDIR,
                "RMSPMI": RMSPMI,
                "balance_index": balance_index,
                "CBS": CBS
            }

            if (RMSPMI < .80) or (RMSPMI < .80):
                balance_output_for_attribute = True
            if balance_index < .80:
                balance_attribute = True

            # RMSDIR : Balance output for attribute
            # RMSPMI : Balance output for attribute
            # balance_index : Balance attribute
