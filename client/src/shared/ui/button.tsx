import styled, { css } from "styled-components";

const Button = styled.button<{
  loading?: boolean;
  disabled?: boolean;
  size: "small" | "big";
}>`
  ${(props) =>
    props.size === "small"
      ? css`
          padding: 0.625rem 1rem;
        `
      : css`
          padding: 1.25rem 2rem;
        `}
  border-radius: 10px;
  position: relative;
  transition: box-shadow 0.1s linear;

  ${(props) =>
    props.disabled
      ? css`
          background-color: grey;
        `
      : css`
          background-color: white;
          &:hover {
            box-shadow: 0 0 5px 5px #ffffff55;
          }
        `}

  ${(props) =>
    props.loading &&
    css`
      &::after,
      &::before {
        box-sizing: initial;
        content: "";
        position: absolute;
        height: 100%;
        width: 100%;
        background-image: conic-gradient(
          from var(--angle),
          #ff4545,
          #00ff99,
          #006aff,
          #ff0095,
          #ff4545
        );
        top: 50%;
        left: 50%;
        translate: -50% -50%;
        z-index: -1;
        padding: 3px;
        border-radius: 10px;
        animation: 3s spin linear infinite;
      }

      &::before {
        filter: blur(1.5rem);
        opacity: 0.5;
      }

      @property --angle {
        syntax: "<angle>";
        initial-value: 0deg;
        inherits: false;
      }

      @keyframes spin {
        from {
          --angle: 0deg;
        }
        to {
          --angle: 360deg;
        }
      }
    `}
`;

export default Button;
