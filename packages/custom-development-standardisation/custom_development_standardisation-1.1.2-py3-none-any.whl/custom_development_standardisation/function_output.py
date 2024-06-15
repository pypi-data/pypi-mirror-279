

def generate_outcome_message(outcome,output,the_type=None):
    if outcome != "success" and outcome != "error":
        raise ValueError("Outcome parameter is not 'success' or 'error'")
    if outcome == "error" and (the_type == None and the_type != "custom" and the_type != "others"):
        raise ValueError("Type of error is not 'custom', 'others', or has not been specified. ")
    if outcome == "success":
        return {"outcome": outcome, "output": output}
    if outcome == "error":
        return {"outcome": outcome, "output": output, "the_type": the_type}



