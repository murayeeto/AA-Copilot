import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// Initialize Firebase (ensure this block is written only once)
const firebaseConfig = {
  apiKey: "AIzaSyBCRWu691eB73T0xWoCRKt4THeFxr3qV9Y",
  authDomain: "aacopilot-55872.firebaseapp.com",
  projectId: "aacopilot-55872",
  storageBucket: "aacopilot-55872.firebasestorage.app",
  messagingSenderId: "845790635418",
  appId: "1:845790635418:web:2e7b35422516b0b61f0623",
  measurementId: "G-D6FB9MEND2"
};

const app = initializeApp(firebaseConfig); // Ensure 'app' is defined only here

// Export Firebase services
export const auth = getAuth(app);
export const provider = new GoogleAuthProvider();
export const db = getFirestore(app);

// Helper functions
export const googleSignIn = async () => {
  try {
    const result = await signInWithPopup(auth, provider);
    return result.user;
  } catch (error) {
    console.error("Google Sign-In Error:", error);
    throw error;
  }
};

export const googleSignOut = async () => {
  try {
    await signOut(auth);
    console.log("User signed out successfully.");
  } catch (error) {
    console.error("Sign-Out Error:", error);
    throw error;
  }
};
