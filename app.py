def search_manual(query):
    best_sentence = None
    best_score = 0
    best_paragraph = None  # Store the paragraph that produced the best sentence
    for paragraph in manual_paragraphs:
        sentences = split_into_sentences(paragraph)
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue
            score = fuzz.partial_ratio(query.lower(), sentence.lower())
            if score > best_score:
                best_score = score
                best_sentence = sentence
                best_paragraph = paragraph  # Save the paragraph context
    threshold = 60  # Adjust as needed
    if best_score < threshold or not best_sentence:
        return ["No relevant information found."]
    # If the best sentence is too short to be informative, return the entire paragraph
    if len(best_sentence) < 50:
        return [best_paragraph]
    else:
        return [best_sentence]
