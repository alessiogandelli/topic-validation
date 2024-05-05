function createButton(label, tweet) {
    const button = document.createElement('button');
    button.textContent = label.charAt(0).toUpperCase() + label.slice(1);
    button.className = label;
    button.addEventListener('click', () => labelTweet(tweet, label));
    return button;
}

function labelTweet(tweet, label) {
    fetch('/label_tweet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tweet: tweet, label: label }),
    }).then(() => {
        // After labeling the tweet, fetch a new one
        updateDocs(); // assuming 'topic' is the topic you want to fetch tweets for
    });

   
}



window.onload = function () {
    populateTopics();
    fetch('/get_tweet')
        .then(response => response.json())
        .then(data => {
            const documentsDiv = document.getElementById('documents');
            const tweetDiv = document.createElement('div');
            tweetDiv.textContent = data.tweet; // assuming the tweet text is in a 'tweet' property
            documentsDiv.appendChild(tweetDiv);
        })
        .catch(error => console.error('Error:', error));

};


function populateTopics() {
    fetch('/get_topics')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('topic-selector');

            // Create default option
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.text = 'Select a Topic';
            select.appendChild(defaultOption);

            // create different select options
            for (const key in data) {
                const option = document.createElement('option');
                option.value = key;
                option.text = data[key];
                select.appendChild(option);
            }

            // add a listener, when the users selects a topic, we fetch the tweets
            select.addEventListener('change', function () {
                let selectedTopic = this.value;

                if (selectedTopic === '') {
                    return;
                }

                selectedTopic = parseInt(selectedTopic);
                if (Number.isInteger(selectedTopic)) {
                    updateDocs();           // fetch tweets for the selected topic
                }
                
            });
        });
}

//get the selected topic and fetch a random tweet for that topic
function updateDocs() {

    const topic = document.getElementById('topic-selector').value;

    console.log('Fetching tweet for topic:', topic);

    fetch(`/get_tweet?topic=${encodeURIComponent(topic)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received data:', data);

            const documentsDiv = document.getElementById('documents');
            if (!documentsDiv) {
                console.error('Could not find the "documents" div');
                return;
            }

            documentsDiv.innerHTML = ''; // Clear any existing documents

            // Create a new tweet element
            const tweetElement = createTweet(data);
            if (!tweetElement) {
                console.error('createTweet did not return a valid element');
                return;
            }
            // Append the tweet element to the documents div
            documentsDiv.appendChild(tweetElement);
        })
        .catch(error => console.error('Error:', error));
}


// create tweet object with text and buttons 
function createTweet(data) {
    console.log(data);
    const tweetDiv = document.createElement('div');
    tweetDiv.className = 'tweet';
    tweetDiv.dataset.id = data.id; // Store the id as a data attribute


    const tweetText = document.createElement('p');
    tweetText.textContent = data.text || 'No text provided';
    tweetDiv.appendChild(tweetText);

    const positiveButton = document.createElement('button');
    positiveButton.className = 'positive';
    positiveButton.textContent = 'Correct';
    positiveButton.addEventListener('click', () => labelTweet(data.id, 'positive'));
    tweetDiv.appendChild(positiveButton);

    const neutralButton = document.createElement('button');
    neutralButton.className = 'neutral';
    neutralButton.textContent = 'not clear';
    neutralButton.addEventListener('click', () => labelTweet(data.id, 'neutral'));
    tweetDiv.appendChild(neutralButton);

    const negativeButton = document.createElement('button');
    negativeButton.className = 'negative';
    negativeButton.textContent = 'Wrong';
    negativeButton.addEventListener('click', () => labelTweet(data.id, 'negative'));
    tweetDiv.appendChild(negativeButton);

    return tweetDiv;
}

// Add a listener to the button view dataframe
document.getElementById('view-dataframe').addEventListener('click', function() {
    var topic = document.getElementById('topic-selector').value;
    if (topic === '') {
        window.location.href = '/get_df';

    }
    window.location.href = '/get_df?topic=' + encodeURIComponent(topic);
});