// Pre-processing of text by removing redundant characters and splitting each word.
function preprocessText(document) {
    return document.toLowerCase().replace(/["'.,\/#!$%\^&\*;:{}=\-_`~()]/g, '').trim().split(/\s+/);
}

// Calculate the word count of the given text.
function calculateWordCount(textWords) {
    const wordCountArray = [];
    
    // Iterate through the textWords array and add counts for occurrences of words.
    for (let i = 0; i < textWords.length; i++) {
        const word = textWords[i];
        const found = wordCountArray.find(element => element.word === word);

        if (found) {
            found.count++;
        } else {
            wordCountArray.push({word: word, count: 1});
        }
    }
    return wordCountArray;
}

// Calculate the dot product of the two sets of words.
function calculateDotProduct(wordCount1, wordCount2) {
    let dotProduct = 0;
    
    //// Iterate through wordCount1 and find matching word pairs in wordCount2.
    for (let i = 0; i < wordCount1.length; i++) {
        const Pair1 = wordCount1[i];
        const found = wordCount2.find(Pair2 => Pair2.word === Pair1.word);

        if (found) {
            dotProduct += Pair1.count * found.count;
        }
    }
    return dotProduct;
}

// Calculate the magnitude of a set of word counts.
function calculateMagnitude(wordCountArray) {
    let magnitude = 0;

    for (let i = 0; i < wordCountArray.length; i++) {
        const wordPair = wordCountArray[i];
        magnitude += wordPair.count * wordPair.count;
    }
    return magnitude;
}

// Generate a HTML table from word count arrays.
function calculateTable(wordCount1, wordCount2) {

    // Create a new set to store words from both documents.
    let combinedWordCount = new Set([...wordCount1.map(a => a.word), ...wordCount2.map(a => a.word)]);

    // Convert the combined set back to array and sort alphabetically.
    let combinedArray = Array.from(combinedWordCount).sort((a, b) => a.localeCompare(b));

    // Start table with headers.
    let tableHTML = `<table id="wordCountTable">
                        <tr>
                          <th class="wordColumn">Word</th>
                          <th class="countColumn">D1</th>
                          <th class="countColumn">D2</th>
                        </tr>`;

    // Iterate over the combined array, adding table rows for each word.
    for (let i = 0; i < combinedArray.length; i++) {
        const word1 = wordCount1.find(wordPair => wordPair.word === combinedArray[i]);
        const word2 = wordCount2.find(wordPair => wordPair.word === combinedArray[i]);

        let count1, count2;

        if (word1) {
            count1 = word1.count;
        } else {
            count1 = 0;
        }

        if (word2) {
            count2 = word2.count;
        } else {
            count2 = 0;
        }

        // Add table row.
        tableHTML += `<tr><td>${combinedArray[i]}</td><td class="D1Column">${count1}</td><td class="D2Column">${count2}</td></tr>`;

    }

    // Close table.
    tableHTML += "</table>";

    return tableHTML;
}

// Process the previous content and calculate the similarity.
function compareTwoText() {
    const Document1 = preprocessText(document.getElementById("Document1").value);
    const Document2 = preprocessText(document.getElementById("Document2").value);

    const wordCount1 = calculateWordCount(Document1);
    const wordCount2 = calculateWordCount(Document2);

    const dotProduct = calculateDotProduct(wordCount1, wordCount2);

    const magnitude1 = calculateMagnitude(wordCount1);
    const magnitude2 = calculateMagnitude(wordCount2);

    // The similarity is calculated using a mathematical formula.
    const Similarity = dotProduct / (Math.sqrt(magnitude1) * Math.sqrt(magnitude2));

    // Call the generateTable function to create a word count table.
    const tableHTML = calculateTable(wordCount1, wordCount2);

    const tableElement = document.getElementById("table");
    const resultsElement = document.getElementById("results");

    // Update the HTML of the "table" and "results" elements.
    tableElement.innerHTML = tableHTML;
    resultsElement.innerHTML = `<h3 class="red-text">Similarity: <span>${(Similarity * 100).toFixed(2)}%</span></h3>`;
}

