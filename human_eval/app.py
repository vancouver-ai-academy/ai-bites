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
    return render_template(f"{args.starting_page}.html")


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# MAIN FUNCTIONS
################


# EVAL FUNCTIONS
# --------------
def get_feedback_path(user, timestamp):
    user_folder = re.sub(r"\W", "_", user)
    feedback_path = os.path.join(args.output_folder, user_folder, timestamp)
    os.makedirs(feedback_path, exist_ok=True)
    return feedback_path


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
        # replace all special characters with "_"
        feedback_path = get_feedback_path(
            user=feedback_data["user"], timestamp=feedback_data["timestamp"]
        )
        map_dict = {
            0: "a",
            1: "b",
            -1: "neither",
            100: "both",
        }
        chosen = map_dict[feedback_data["choice"]]
        comment = feedback_data["text"]
        feedback_fname = os.path.join(feedback_path, "feedback.json")
        feedback_dict = {
            "chosen": chosen,
            "comment": comment,
            "timestamp": feedback_data["timestamp"],
            "question": feedback_data["question"],
        }
        save_json(feedback_fname, feedback_dict)
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


# def load_predictions(path):
#     """
#     To be customized by user
#     """
#     import pandas as pd

#     df = pd.read_csv("static/datasets/llm_samples_E5_nq_train 2.csv")
#     pred_list = []
#     for i in range(len(df)):
#         pred_dict = df.iloc[i].to_dict()
#         pred_list.append(pred_dict)

#     # img_list = glob.glob(os.path.join(path, "*", "*.jpg"))
#     # img_list = [{"img_path": img} for img in img_list]
#     # assert len(img_list) > 0, f"No images found in {path}"

#     return pred_list


# @app.route("/eval_get_insight_cards", methods=["POST"])
# def eval_get_insight_cards():
#     """
#     Render the main page.

#     Returns:
#         str: Rendered HTML for the main page.
#     """
#     response = request.get_json()
#     data = {}

#     # get image predictions
#     model_1_preds = load_predictions(args.model_1_preds)
#     # model_2_preds = load_predictions(args.model_2_preds)

#     # get random index
#     ind = np.random.choice(len(model_1_preds))
#     model_a = model_1_preds[ind]
#     # # coin flip
#     # if np.random.rand() > 0.5:
#     #     model_a = model_1_preds[ind]
#     #     model_b = model_2_preds[ind]
#     # else:
#     #     model_a = model_2_preds[ind]
#     #     model_b = model_1_preds[ind]

#     # assert all exist
#     # model_a["instruction"] = model_a["instruction"].replace("\n", "<br>")
#     data["insight_card_a"] = render_template(
#         "fragments/output_card.html",
#         model_output=model_a,
#         id="A",
#     )

#     # data["insight_card_b"] = render_template(
#     #     "fragments/output_card.html",
#     #     model_output=model_b,
#     #     id="B",
#     # )

#     data["task"] = args.task_name
#     data["timestamp"] = str(time.time()).replace(".", "")

#     feedback_path = os.path.join(args.output_folder, data["timestamp"])
#     os.makedirs(feedback_path, exist_ok=True)

#     # save in json file
#     save_json(os.path.join(feedback_path, "model_a.json"), model_a)
#     # save_json(os.path.join(feedback_path, "model_b.json"), model_b)
#     # save_json(
#     #     os.path.join(feedback_path, "feedback.json"), {"choice": "", "comment": ""}
#     # )
#     print("saved in ", feedback_path)
#     return jsonify(data)


def load_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data


def get_image_preds_bigdoc(path, task):
    """
    To be customized by user
    """

    # loop over folders
    img_list = []
    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        image_input = os.path.join(folder_path, "image.png")
        image_meta = load_json(os.path.join(folder_path, f"{folder}.json"))
        if (
            task == "chart2summary"
            and image_meta["dataset_name"] == "BigDocChart2Summary"
        ):
            # task = "chart2summary"
            img_list += [
                {
                    "path": path,
                    "prompt": image_meta["user_input"]["content"],
                    "image_input": image_input,
                    "text_output": image_meta["output"],
                }
            ]
        else:
            image_output = os.path.join(folder_path, f"{task}.png")
            if not os.path.exists(image_output):
                continue
            img_list += [
                {
                    "path": path,
                    "prompt": image_meta["user_input"]["content"],
                    "image_input": image_input,
                    "image_output": image_output,
                }
            ]

    assert len(img_list) > 0, f"No images found in {path}"
    print("Found ", len(img_list), " images")
    return img_list


@app.route("/eval_get_insight_cards", methods=["POST"])
def eval_get_insight_cards_bigdoc():
    """
    Render the main page.

    Returns:
        str: Rendered HTML for the main page.
    """
    response = request.get_json()
    task = np.random.choice(["html2image", "svg2image", "flow2image", "chart2summary"])
    data = {"user": response["user"]}

    # task = "chart2summary"
    # get image predictions
    model_1_images = get_image_preds_bigdoc(args.model_1_preds, task)
    model_2_images = get_image_preds_bigdoc(args.model_2_preds, task)

    # get random index
    ind = np.random.choice(len(model_1_images))
    # coin flip
    if np.random.rand() > 0.5:
        model_a = model_1_images[ind]
        model_b = model_2_images[ind]
    else:
        model_a = model_2_images[ind]
        model_b = model_1_images[ind]

    # assert all exist
    if task == "chart2summary":
        card = "example_fragments/bigdoc_text_card.html"
    else:
        card = "example_fragments/bigdoc_card.html"

    data["insight_card_a"] = render_template(
        card,
        model_output=model_a,
        id="A",
    )

    data["insight_card_b"] = render_template(
        card,
        model_output=model_b,
        id="B",
    )

    data["task"] = task
    data["timestamp"] = str(time.time()).replace(".", "_")
    data["criterion"] = map_task_to_criterion(task)
    feedback_path = get_feedback_path(user=data["user"], timestamp=data["timestamp"])
    # save model a and be
    save_json(os.path.join(feedback_path, "meta.json"), {"task": task})
    save_json(os.path.join(feedback_path, "model_a.json"), model_a)
    save_json(os.path.join(feedback_path, "model_b.json"), model_b)
    print("saved in ", feedback_path)
    return jsonify(data)


def map_task_to_criterion(task):
    if task == "html2image":
        return "Evaluate based on how clode the image in 'Model Output' is to '(3) Model Input'"

    elif task == "svg2image":
        return "Evaluate based on how clode the image in 'Model Output' is to '(3) Model Input'"

    # pdf2latex

    elif task == "flow2image":
        return (
            "Evaluate based on how the node names and edges in 'Model Output' is close to '(3) Model Input',"
            + "please disregard colors and orientation"
        )

    elif task == "chart2summary":
        return "Are the facts and numbers in the summary consistent with the information in the chart image?"


if __name__ == "__main__":
    # create port args
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=7883)
    parser.add_argument("-s", "--starting_page", type=str, default="paired_output")
    parser.add_argument("-o", "--output_folder", type=str, default="results")
    parser.add_argument(
        "-m1",
        "--model_1_preds",
        type=str,
        default="static/datasets/phi3_bigdoc",
    )
    parser.add_argument(
        "-m2",
        "--model_2_preds",
        type=str,
        default="static/datasets/phi3_bigdoc",
    )

    # parser.add_argument(
    #     "-t",
    #     "--task",
    #     type=str,
    #     default="svg2image",
    # )

    args = parser.parse_args()

    app.run(debug=True, port=args.port, host="0.0.0.0", use_reloader=False)
