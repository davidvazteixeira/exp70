/*
Using lib MFRC522 v1.4.0 from GithubCommunity

SDA:  10
SCK:  13
MOSI: 11
MISO: 12
RST:  9

GND
3.3V  <=   !!!!!!!!!!! 

*/

#include <require_cpp11.h>
#include <MFRC522Extended.h>
#include <MFRC522.h>
#include <deprecated.h>
#include <EEPROM.h>

enum {
  PERM_USER,
  PERM_MANAGER,
  PERM_ADMIN
};

enum {
  PYTHON_MODE,
  TERMINAL_MODE
};

// Arduino: The hardware SS pin. Nano: 10, Mega: 53
// RFID Board: The SDA Pin on 
#define SS 53      

// Any digital
#define RST 49 

MFRC522 rfid(SS, RST);

#define CARDS 4 // Up to 100
byte password[CARDS][10] = {0};
byte permission[CARDS] = {PERM_USER};
byte readPassword[10] = {0};
byte readPermission = PERM_USER;

int psize = 0;

#define CHECKMODE 0
#define ADDMODE 1
byte nextReadMode = CHECKMODE;
byte nextPermission = PERM_USER;

byte send_mode = PYTHON_MODE;

void setup() {
  Serial.begin(115200);

  if (send_mode == TERMINAL_MODE) Serial.print("init MFRC522...");
  
  SPI.begin();
  rfid.PCD_Init();
  
  if (send_mode == TERMINAL_MODE) Serial.println("done");
  
  loadCardsFromEEPROM();

  if (send_mode == TERMINAL_MODE) askCardMessage();
}

void loadCardsFromEEPROM(){
  for(int card=0; card<CARDS; card++){
    for(int i=0; i< 10; i++){
       password[card][i] = EEPROM.read(i + card*11);
    }
    permission[card] = EEPROM.read(10 + card*11);
  }
}

void saveCardsToEEPROM(){
  for(int card=0; card<CARDS; card++){
    for(int i=0; i< 10; i++){
       EEPROM.write(i + card*11, password[card][i]);
    }
    EEPROM.write(10 + card*11, permission[card]);
  }
}

void serialEvent(){
  if(send_mode == PYTHON_MODE){
    switch(Serial.read()){
    case 'm':
      send_mode = TERMINAL_MODE;
      Serial.println("Terminal mode on");
      break;
    }
    return;
  }

  if(send_mode == TERMINAL_MODE){
    switch(Serial.read()){
    case 'a':
      delay(100);
      nextPermission = Serial.parseInt();
      Serial.print("Permission: ");
      Serial.println(nextPermission);
      nextReadMode = ADDMODE;
      Serial.println("Add user mode");
      break;
    case 'c':
      nextReadMode = CHECKMODE;
      Serial.println("Check user mode");
      break;
    case 'r':
      Serial.print("Reset...");
      for(int card=0; card<CARDS; card++){
        for(int i=0; i<10; i++) password[card][i] = 0;
        permission[card] = PERM_USER;
      }
      Serial.println("done.");
      break;
    case 'S':
      Serial.print("Saving...");
      saveCardsToEEPROM();
      Serial.println("done.");
      break;
    case 'L':
      Serial.print("Loading...");
      loadCardsFromEEPROM();
      Serial.println("done.");
      break;
    case 'E':
      printEEPROM();
      Serial.println("done.");
      break;
    case 'F':
      Serial.print("Formating EEPROM...");
      for(int i = 0; i<CARDS*11;i++) EEPROM.write(i, 0);
      Serial.println("done.");
      break;
    case 'p':
      Serial.println("Cards:");
      for(int card=0; card<CARDS; card++){
        printCard(card);
        Serial.println();
      }
      break;
    case 'm':
      send_mode = PYTHON_MODE;
      break;      
    }
    return;
  }
}

int findBlankPosition(){
  bool blank;
  for(int card=0; card<CARDS;card++){
    blank = true;
    for(int i=0; i<10;i++){
      if(password[card][i] != 0){
        blank = false;
        break;  
      }
    }
    if(blank){
      Serial.print("Blank space position: ");
      Serial.println(card);
      return card; 
    }  
  }
  return -1;
}

int searchCard(){
  bool ok;
  for(int card=0; card<CARDS;card++){
    ok = true;
    for(int i=0; i<10;i++){
      if(password[card][i] != readPassword[i]){
        ok = false;
        break;  
      }
    }
    if(ok){
      return card; 
    }  
  }
  return -1;
}

int addCard(){
  if (searchCard() >= 0) {
    Serial.println("Already in system");
    return -1;
  }
  
  int card = findBlankPosition();
  if(card >= 0){
    for(int i=0; i<10; i++) password[card][i] = readPassword[i];
    permission[card] = nextPermission;
    return card;
  } else {
    return -1;
  }
}

void checkPresence(){
  if ( ! rfid.PICC_IsNewCardPresent()) return;  // Look for new cards
  if ( ! rfid.PICC_ReadCardSerial()) return;    // Select one of the cards

  for(byte i=0; i<10; i++) readPassword[i] = 0;
  for (byte i = 0; i < rfid.uid.size; i++) readPassword[i] = rfid.uid.uidByte[i];

  if(send_mode == PYTHON_MODE) processCardSilence();
  if(send_mode == TERMINAL_MODE) processCardVerbose();

  delay(2000);
}

void processCardVerbose(){
  int card;
  switch(nextReadMode){
  case ADDMODE:
    card = addCard();
    if(card >= 0){
      Serial.println("Code saved!");
      printCard(card);
      nextReadMode = CHECKMODE;
      Serial.println();
      Serial.println("Check user mode");
    } else {
      Serial.println("Error.");
    }
    break;

  case CHECKMODE:
    card = searchCard();
    if(card >= 0) {
      Serial.println(" CHECKED!");
      printCard(card);
      Serial.println();
    } else {
      Serial.println("NOT in system.");
    }
    break;
  }
  askCardMessage();  
}

void processCardSilence(){
  int card = searchCard();
  if(card >= 0) {
    printCardCompact(card);
  } else {
    Serial.println('x');
  }
}

bool checkPassword(int card){
  for(int i=0; i<10; i++) if(password[card][i] != readPassword[i]) return false;
  return true;  
}

void printReadCode(int card){
  for(int i=0; i<10; i++) {
      Serial.print(readPassword[i]);    
      Serial.print(" "); 
  }
}

void printCard(int card){
  Serial.print("Card <");
  Serial.print(card);
  Serial.print("> :");
  for(int i=0; i<10; i++) {
    byte code = password[card][i];
    if(code < 16) Serial.print('0');
    Serial.print(code, HEX);    
    Serial.print(' '); 
  }
  Serial.print(" - ");
  Serial.print(permission[card]);        
}

void printCardCompact(int card){
  for(int i=0; i<10; i++) {
    byte code = password[card][i];
    if(code < 16) Serial.print('0');
    Serial.print(code, HEX);    
  }
  Serial.println();
}


void printEEPROM(){
  for(int card=0; card<CARDS;card++){
    for(int i=0; i<10; i++){
      byte code = EEPROM.read(i + card*11);
      if(code < 16) Serial.print('0');
      Serial.print(code, HEX);
      Serial.print(' ');
    }
    Serial.print(" - ");
    Serial.print(EEPROM.read(10 + card*11));
    Serial.println();
  }
}

void askCardMessage(){
  Serial.println("Insert tag");  
}

void loop() {
  checkPresence();
} 
