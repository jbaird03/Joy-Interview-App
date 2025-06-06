import React, { useEffect, useState } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import type { Email } from './types';

const App = () => {
  const [emails, setEmails] = useState<Email[]>([]);
  const [selectedEmail, setSelectedEmail] = useState<Email | null>(null);
  const [editedReply, setEditedReply] = useState<string>("");
  const [loadingSuggestion, setLoadingSuggestion] = useState<boolean>(false);
  const [showSentMessage, setShowSentMessage] = useState<boolean>(false);

  useEffect(() => {
    axios.get("/emails").then((res) => {
      setEmails(res.data);
    });
  }, []);

  const suggestReply = (body: string, patient_name: string) => {
    setLoadingSuggestion(true);
    axios.post("/suggest", { body, patient_name }).then((res) => {
      setEditedReply(res.data.suggested);
      setLoadingSuggestion(false);
    });
  };

  const sendEmail = () => {
    if (!selectedEmail) return;

    // Create a new email object with updated reply
    const updatedEmail: Email = {
      ...selectedEmail,
      reply: editedReply,
    };

    axios.post("/send", updatedEmail).then(() => {
      setShowSentMessage(true);
      setSelectedEmail(null); // Close out the email view
      setTimeout(() => setShowSentMessage(false), 3000);
    });
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl mb-4">Inbox</h1>
      <ul>
        {emails.map((email) => (
          <li
            key={email.id}
            className="cursor-pointer"
            onClick={() => {
              setSelectedEmail(email);
              suggestReply(email.body, email.patient_name);
            }}
          >
            {email.subject} - {email.patient_name}
          </li>
        ))}
      </ul>

      {selectedEmail && (
        <div className="mt-4">
          <h2 className="text-xl">{selectedEmail.subject}</h2>
          <p className="mb-2">{selectedEmail.body}</p>
          {loadingSuggestion ? (
            <div className="text-gray-500 italic mb-2 animate-pulse">
              Generating AI reply...
            </div>
          ) : (
            <>
              <textarea
                className="w-full border p-2"
                rows={20}
                value={editedReply}
                onChange={(e) => setEditedReply(e.target.value)}
              />
              <Button className="mt-2" onClick={sendEmail}>
                Send
              </Button>
            </>
          )}
        </div>
      )}

      {showSentMessage && (
        <div className="mt-4 text-green-600 font-semibold">
          Email sent successfully!
        </div>
      )}
    </div>
  );
};

export default App;
