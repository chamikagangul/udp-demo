import app from "./app.mjs";

const PORT = parseInt(process.env.PORT) || 6000;

app.listen(PORT, () => {
  console.log(`listening on http://localhost:${PORT}`);
});
