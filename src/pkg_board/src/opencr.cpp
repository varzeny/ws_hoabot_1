#include "pkg_board/opencr.hpp"



NodeBoard::NodeBoard() : Node("node_board"), serial(io_service,"/dev/ttyACM0")
{
    serial.set_option(boost::asio::serial_port_base::baud_rate(115200));
    data_toBoard.resize(2);

    subscriber_board_cmd = this->create_subscription<std_msgs::msg::String>(
        "board_cmd",
        10,
        std::bind(
            &NodeBoard::callback_board_cmd,
            this,
            std::placeholders::_1
        )
    );

}


NodeBoard::~NodeBoard(){

}

void NodeBoard::callback_board_cmd(const std_msgs::msg::String::SharedPtr msg){

    RCLCPP_INFO(this->get_logger(),msg->data);
    
    if (msg->data == "stop") {
        data_toBoard[0] = 0;
        data_toBoard[1] = 0;
    } else if (msg->data == "w") {
        data_toBoard[0] = 50;
        data_toBoard[1] = 50;
    } else if (msg->data == "a") {
        data_toBoard[0] = -50;
        data_toBoard[1] = 50;
    } else if (msg->data == "s") {
        data_toBoard[0] = -50;
        data_toBoard[1] = -50;
    } else if (msg->data == "d") {
        data_toBoard[0] = 50;
        data_toBoard[1] = -50;
    } else {
        // 일치하는 명령이 없을 때의 처리
    }

    //  시리얼 포트로 전송
    toBoard(data_toBoard);

    return;
}

void NodeBoard::toBoard(const std::vector<int32_t>& data){
    std::string buffer = "<";
    boost::asio::write(serial, boost::asio::buffer(buffer)); // '<' 문자 전송

    for (auto value : data) {
        boost::asio::write(serial, boost::asio::buffer(&value, sizeof(int32_t)));
    }
}




int main(int argc, char* argv[]){

    rclcpp::init(argc,argv);
    auto node = std::make_shared<NodeBoard>();
    rclcpp::spin(node);
    rclcpp::shutdown();

    return 0;
}
