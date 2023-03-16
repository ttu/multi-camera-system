import { QueryClient, QueryClientProvider } from "react-query";
import "./App.css";
import MainComponent from "./MainComponent";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <MainComponent />
    </QueryClientProvider>
  );
}

export default App;
