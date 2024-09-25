import sys, os
import glob

from flask import Flask, request, render_template, jsonify, session
import os, re
import json
import pandas as pd
import copy, time
import numpy as np


form_questions = {}
# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["JSON_FOLDER"] = "static/json"
app.config["OUTPUT_FOLDER"] = "static/outputs"
app.config["FEEDBACK_FOLDER"] = "feedback_cba"
app.config["RESULTS_FOLDER"] = "results"
app.config["STUDY_FOLDER"] = "static/human_study"
app.config["USERS_FOLDER"] = "static/users"
app.config["DATA_FOLDER"] = "static/datasets"


@app.route("/")
def index():
    """
    Render the index page.

    Returns:
        str: Rendered HTML for the index page.
    """
    return render_template(f"index.html")


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# MAIN FUNCTIONS
################


def get_user_data_folder(request):
    response = request.get_json()
    dataset_name = response["dataset"]
    user_name = response["user"]
    user_data_folder = os.path.join(app.config["USERS_FOLDER"], user_name, dataset_name)
    return user_data_folder


# EVAL FUNCTIONS
# --------------


@app.route("/eval_page")
def eval_page():

    return render_template("eval_arcade.html")


@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    """
    Handle submission of feedback data.

    Returns:
        JSON response: Success or error message.
    """

    # Parse the JSON data from the request
    feedback_data = request.get_json()
    user_data_folder = get_user_data_folder(request)
    insight_id = feedback_data.get("insight").split("-")[-1]
    output_folder = os.path.join(user_data_folder, f"insight_card_{insight_id}")
    insight_dict = json.load(open(os.path.join(output_folder, "insight_dict.json")))

    output_file = os.path.join(output_folder, "feedback.json")
    # feedback_data["insight_dict"] = insight_dict
    with open(output_file, "w") as f:
        json.dump(feedback_data, f, indent=4)
    print(f"feedback saved in {output_file}")
    return jsonify({"status": "success", "message": "Feedback submitted successfully!"})


@app.route("/submit-feedback-compare", methods=["POST"])
def submit_feedback_compare():
    """
    Handle submission of feedback data.
    Returns:
        JSON response: Success or error message.
    """
    try:
        # Parse the JSON data from the request
        feedback_data = request.get_json()
        feedback_path = os.path.join(
            app.config["STUDY_FOLDER"], feedback_data["timestamp"]
        )
        assert os.path.exists(feedback_path)
        map_dict = {0: "A", 1: "B", -1: "neither", 99: "both"}
        chosen = map_dict[feedback_data["choice"]]
        comment = feedback_data["text"]
        feedback_fname = os.path.join(feedback_path, "feedback.json")
        feedback_dict = {
            "chosen": chosen,
            "comment": comment,
            "timestamp": feedback_data["timestamp"],
            "question": feedback_data["question"],
        }
        ut.save_json(feedback_fname, feedback_dict)
        print(feedback_dict)
        print("Saved in ", feedback_fname)

        # Return a success response
        return jsonify(
            {"status": "success", "message": "Feedback submitted successfully!"}
        )

    except Exception as e:
        # Handle any errors that occur
        print("Error:", e)
        return (
            jsonify({"status": "error", "message": "Failed to submit feedback."}),
            500,
        )


@app.route("/main")
def main():
    """
    Render the main page.

    Returns:
        str: Rendered HTML for the main page.
    """
    return render_template("main.html")


def load_predictions(path):
    """
    To be customized by user
    """
    img_list = glob.glob(os.path.join(path, "*", "*.jpg"))
    img_list = [{"img_path": img} for img in img_list]
    assert len(img_list) > 0, f"No images found in {path}"

    return img_list


@app.route("/eval_get_insight_cards", methods=["POST"])
def eval_get_insight_cards():
    """
    Render the main page.

    Returns:
        str: Rendered HTML for the main page.
    """
    response = request.get_json()
    data = {}

    # get image predictions
    model_1_preds = load_predictions(args.model_1_preds)
    model_2_preds = load_predictions(args.model_2_preds)

    # get random index
    ind = np.random.choice(len(model_1_preds))
    # coin flip
    if np.random.rand() > 0.5:
        model_a = model_1_preds[ind]
        model_b = model_2_preds[ind]
    else:
        model_a = model_2_preds[ind]
        model_b = model_1_preds[ind]

    # assert all exist

    data["insight_card_a"] = render_template(
        "fragments/output_card.html",
        model_output=model_a,
        id="A",
    )

    data["insight_card_b"] = render_template(
        "fragments/output_card.html",
        model_output=model_b,
        id="B",
    )

    data["task"] = args.task_name
    data["timestamp"] = str(time.time()).replace(".", "")

    feedback_path = os.path.join(args.output_folder, data["timestamp"])
    os.makedirs(feedback_path, exist_ok=True)

    # save in json file
    save_json(os.path.join(feedback_path, "model_a.json"), model_a)
    save_json(os.path.join(feedback_path, "model_b.json"), model_b)
    save_json(
        os.path.join(feedback_path, "feedback.json"), {"chosen": "", "comment": ""}
    )
    print("saved in ", feedback_path)
    return jsonify(data)


if __name__ == "__main__":
    # create port args
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=7879)
    parser.add_argument("-s", "--starting_page", type=str, default="eval")
    parser.add_argument("-o", "--output_folder", type=str, default="results")
    parser.add_argument(
        "-m1",
        "--model_1_preds",
        type=str,
        default="static/datasets/csm/model_1_preds",
    )
    parser.add_argument(
        "-m2",
        "--model_2_preds",
        type=str,
        default="static/datasets/csm/model_2_preds",
    )

    parser.add_argument(
        "-t",
        "--task_name",
        type=str,
        default="Plot Generation",
    )

    args = parser.parse_args()
    if args.starting_page == "eval":
        starting_page = "eval_comparison"
    else:
        starting_page = "index"

    app.run(debug=True, port=args.port, host="0.0.0.0", use_reloader=False)
