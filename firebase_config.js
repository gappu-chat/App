const firebaseConfig = {
  apiKey: "AIzaSyDFmI6YZIp7qKbgrgdr8VPLr1xkOXbGHb0",
  authDomain: "auction-game-80e14.firebaseapp.com",
  databaseURL: "https://auction-game-80e14-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "auction-game-80e14",
  appId: "1:984901985057:web:8a5d78169ad75f72341460"
};
firebase.initializeApp(firebaseConfig);
firebase.auth().setPersistence(firebase.auth.Auth.Persistence.LOCAL);
const auth = firebase.auth();
const db = firebase.database();
