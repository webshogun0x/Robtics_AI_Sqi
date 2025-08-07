function onFormSubmit(e) {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var lastRow = sheet.getLastRow();
    var data = sheet.getRange(lastRow, 1, 1, 7).getValues()[0]; // Timestamp, Name, ID, Component, Quantity, Consumable, Photo
    var component = data[3];
    var quantity = parseInt(data[4]);
    var consumable = data[5] === 'Yes';
  
    // Validate input
    if (!component || isNaN(quantity) || quantity <= 0) {
      sendEmail('Invalid entry: Check component or quantity.');
      return;
    }
  
    // Update stock (for consumables)
    if (consumable) {
      var stockRange = sheet.getRange('A2:B10'); // Adjust range for stock list
      var stockData = stockRange.getValues();
      for (var i = 0; i < stockData.length; i++) {
        if (stockData[i][0] === component) {
          var currentStock = parseInt(stockData[i][1]);
          var newStock = currentStock - quantity;
          stockRange.getCell(i + 1, 2).setValue(newStock);
          sheet.getRange(lastRow, 8).setValue(newStock); // Update Stock Remaining
          if (newStock < 10) {
            sendEmail(`Low stock alert: ${component} has ${newStock} units left.`);
          }
          break;
        }
      }
    }
  }
  
  function sendEmail(message) {
    MailApp.sendEmail({
      to: 'your_email@example.com',
      subject: 'Inventory Alert',
      body: message
    });
  }