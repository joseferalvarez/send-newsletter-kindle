# utils/get_label_ids.py

def get_label_ids(labels, selected_labels):
  """Get ids of the labels selected in the YAML file"""
  selected_ids = []

  for label in labels:
    for selected_label in selected_labels:
      if label["name"] == selected_label:
        selected_ids.append(label["id"])

  return selected_ids