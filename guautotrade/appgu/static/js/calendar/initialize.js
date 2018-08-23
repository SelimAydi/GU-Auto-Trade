// Please note that the months start from index 0. So August would be 7, not 8

// $.getJSON("/api/events/", saveJSON);

// function getJSON(api){
//     $.getJSON(api, saveJSON);
// }

function saveJSON(result){
    if (result.length === 0){
        console.log("no events");
          caleandar(document.getElementById('caleandar'), null, {});
    } else {
        console.log("there are events");
        var dateparts = (result[0]['fields']['date']).split('-');

        var eventsx = [];

        for (var i = 0; i < result.length; i++){
        var datex = (result[i]['fields']['date']).split('-');

        eventsx.push(
            {
                'Date': new Date(datex[0], datex[1] - 1, datex[2]),
                'Title': result[i]['fields']['title'],
                'Description': result[i]['fields']['description'],
                'Link': result[i]['fields']['link']
            }
        )
        }

        var events = [
        {'Date': new Date(dateparts[0], dateparts[1] - 1, dateparts[2]), 'Title': 'Shelby Drag Race at 3:25pm.', 'Description': 'Lorem Ipsum'},
        {'Date': new Date(2018, 6, 28), 'Title': 'Another Shelby event!', 'Link': 'https://shelby.com'},
        {'Date': new Date(2018, 7, 27), 'Title': '25 year anniversary Shelby', 'Link': 'https://www.google.com.au/#q=anniversary+gifts'},
        ];

        initialize(eventsx);
    }
}

function initialize(events){
  var settings = {};
  var element = document.getElementById('caleandar');
  caleandar(element, events, settings);
}

