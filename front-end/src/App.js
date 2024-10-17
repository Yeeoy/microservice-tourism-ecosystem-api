import React, { Suspense } from "react";
import { RouterProvider } from "react-router-dom";
import router from "./router";
import { AuthProvider } from "./context/authContext";

function App() {
    return (
        <AuthProvider>
            <Suspense fallback={<div>Loading...</div>}>
                <RouterProvider router={router} />
            </Suspense>
        </AuthProvider>
    );
}

export default App;
