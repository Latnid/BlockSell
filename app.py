import streamlit as st

# 在 Streamlit 应用的侧边栏中加载 MetaMask 插件的 JavaScript 文件
st.sidebar.markdown("""
    <script src="https://cdn.jsdelivr.net/npm/@metamask/metamask-extension@5.5.5/dist/metamask.min.js"></script>
""", unsafe_allow_html=True)

if st.button("Sign with MetaMask"):
  # 询问用户要签名的消息
  message = st.text_input("Enter the message to sign:")
  
  # 调用 MetaMask 签名消息的函数
  window.ethereum.send({
    method: 'personal_sign',
    params: [message],
    from: window.ethereum.selectedAddress
  }, (error, result) => {
    if (error) {
      console.error(error);
    } else {
      # 将签名的结果发送给服务器
      sendSignatureToServer(result);
    }
  });
