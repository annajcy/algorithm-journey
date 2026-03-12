document$.subscribe(function () {
  if (typeof mermaid === "undefined") {
    return;
  }
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "loose",
    theme: "default"
  });
  mermaid.run({
    querySelector: ".mermaid"
  });
});
