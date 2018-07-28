// Please note that the months start from index 0. So August would be 7, not 8

var events = [
  {'Date': new Date(2018, 6, 7), 'Title': 'Shelby Drag Race at 3:25pm.', 'Description': 'Lorem Ipsum'},
  {'Date': new Date(2018, 6, 28), 'Title': 'Another Shelby event!', 'Link': 'https://shelby.com'},
  {'Date': new Date(2018, 7, 27), 'Title': '25 year anniversary Shelby', 'Link': 'https://www.google.com.au/#q=anniversary+gifts'},
];
var settings = {};
var element = document.getElementById('caleandar');
caleandar(element, events, settings);
