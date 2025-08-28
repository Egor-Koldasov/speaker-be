import { useMutation, useQuery } from "convex/react";
import { api } from "langtools-convex";
import { useState } from "react";
import { Button, Text, TextInput, View } from "react-native";



export default function Index() {
  const messages = useQuery(api.publicMessages.get);
  const sendMessage = useMutation(api.publicMessages.send);
  const [text, setText] = useState("");

  const handleSend = async () => {
    if (text.trim()) {
      await sendMessage({ text: text.trim() });
      setText("");
    }
  };

  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        padding: 20,
      }}
    >
      <Text style={{ fontSize: 18, marginBottom: 20 }}>Messages</Text>
      {messages?.map((message) => (
        <Text key={message._id} style={{ marginBottom: 10 }}>
          {message.text}
        </Text>
      ))}
      
      <View style={{ width: "100%", marginTop: 20 }}>
        <TextInput
          style={{
            borderWidth: 1,
            borderColor: "#ccc",
            padding: 10,
            marginBottom: 10,
            borderRadius: 5,
          }}
          value={text}
          onChangeText={setText}
          placeholder="Enter your message..."
        />
        <Button title="Send Message" onPress={handleSend} />
      </View>
    </View>
  );
}
