def search_manual(query):
    best_sentence = None
    best_score = 0
    # Iterate over each paragraph and then each sentence
    for paragraph in manual_paragraphs:
        sentences = split_into_sentences(paragraph)
        for sentence in sentences:
            sentence = sentence.strip()
            # Skip sentences that are too short (e.g., less than 10 characters)
            if len(sentence) < 10:
                continue
            score = fuzz.partial_ratio(query.lower(), sentence.lower())
            if score > best_score:
                best_score = score
                best_sentence = sentence
    threshold = 60  # Adjust this threshold as needed
    if best_score < threshold or not best_sentence:
        return ["No relevant information found."]
    else:
        return [best_sentence]
