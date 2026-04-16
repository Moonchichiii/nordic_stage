import { render, screen } from "@testing-library/react";
import Home from "../src/app/page";

describe("Home page", () => {
  it("renders the starter heading", () => {
    render(<Home />);
    expect(
      screen.getByText(/to get started, edit the page\.tsx file\./i),
    ).toBeInTheDocument();
  });
});