import torch.nn.functional as F
import utils as ut

from optimum.quanto import quantize, freeze
from optimum import quanto


from transformers import AutoTokenizer, AutoModelForSequenceClassification


def main(text="quantization is awesome"):
    # constants
    model_name = "assemblyai/distilbert-base-uncased-sst2"
    quanto_dtype = quanto.qint8

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    print("\nBefore Quantization:\n==================")
    _, _, size_before = predict(model, tokenizer, text)

    print("\nQuantizing the model...\n")
    quantize(model, weights=quanto_dtype, activations=None, bias=None, inplace=True)
    freeze(model)

    print(f"\nAfter Quantization (with {quanto_dtype}):\n==================")
    _, _, size_after = predict(model, tokenizer, text)

    print(f"\nModel Size Reduced by {size_before[''] / size_after['']:.2f}x")


def predict(model, tokenizer, text):
    tokenized_segments = tokenizer(
        [text],
        return_tensors="pt",
        padding=True,
        truncation=True,
    )
    x, x_att = (
        tokenized_segments.input_ids,
        tokenized_segments.attention_mask,
    )

    # make predictions
    model_predictions = F.softmax(
        model(
            input_ids=x,
            attention_mask=x_att,
        )["logits"],
        dim=1,
    )

    # With Module Sizes
    module_sizes = ut.compute_module_sizes(model)
    print(f"The model size is {module_sizes[''] * 1e-9:.2f} GB")

    # Print the probabilities of sentiment
    pos_prob = model_predictions[0][1].item() * 100
    neg_prob = model_predictions[0][0].item() * 100
    print(f"\nThe sentiment of '{text}' is:")
    print(f"Positive: {pos_prob:.1f}%")
    print(f"Negative: {neg_prob:.1f}%")

    return pos_prob, neg_prob, module_sizes


if __name__ == "__main__":
    main(text="quantization is awesome")
