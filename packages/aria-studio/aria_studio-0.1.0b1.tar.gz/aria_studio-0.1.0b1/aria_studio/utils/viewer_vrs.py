# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import argparse
import logging
import os
import typing

import numpy as np
import rerun as rr
from projectaria_tools.core import data_provider
from projectaria_tools.core.sensor_data import SensorData, SensorDataType, TimeDomain
from projectaria_tools.core.stream_id import StreamId

logger = logging.getLogger(__name__)

# Sensor labels used in aria glasses
_CAMERA_RGB_LABEL: str = "camera-rgb"
_CAMERA_ET_LABEL: str = "camera-et"
_CAMERA_SLAM_LEFT_LABEL: str = "camera-slam-left"
_CAMERA_SLAM_RIGHT_LABEL: str = "camera-slam-right"
_IMU_LEFT_LABEL: str = "imu-left"
_IMU_RIGHT_LABEL: str = "imu-right"
_MAGNETOMETER_LABEL: str = "mag0"
_DEFAULT_MEMORY_LIMIT: str = "2GB"


def pars_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vrs", type=str, required=True, help="path to vrs file")
    parser.add_argument(
        "--imu_skip_count",
        "-s",
        type=int,
        default=1,
        help="IMU and Gyro subsampling rate",
    )
    parser.add_argument(
        "--down_sampling_factor",
        "-d",
        type=int,
        default=1,
        help="Downsampling factor for image data",
    )
    parser.add_argument(
        "--jpeg_quality",
        "-q",
        type=int,
        default=100,
        choices=range(1, 101),
        help="JPEG quality for JPEG compression",
    )
    parser.add_argument(
        "--memory_limit",
        "-m",
        type=str,
        default=_DEFAULT_MEMORY_LIMIT,
        help="Memory limit for rerun",
    )
    return parser.parse_args()


def check_args(args: argparse.Namespace) -> None:

    # check if file path exists
    if os.path.exists(args.vrs):
        logger.info("using vrs file {}".format(args.vrs))
    else:
        logger.error("vrs file does not exist")
        exit(1)

    # check validity of imu and dsf args
    if args.imu_skip_count < 1 or args.down_sampling_factor < 1:
        logger.error("imu_skip_count and down_sampling_factor must be greater than 1 ")
        exit(1)


def load_img_data(
    data: typing.Iterator[SensorData], down_sampling_factor: int
) -> np.ndarray:
    img = data.image_data_and_record()[0].to_numpy_array()
    img = img[::down_sampling_factor, ::down_sampling_factor]
    return img


def log_to_rerun(args: argparse.Namespace) -> None:

    # create provider,activate streams and check validity
    provider = data_provider.create_vrs_data_provider(args.vrs)

    if provider is None:
        logger.error("Failed to create a provider")
        exit(1)

    streams_in_vrs = provider.get_all_streams()
    # create deliver options and deactivate all streams
    deliver_option = provider.get_default_deliver_queued_options()
    deliver_option.deactivate_stream_all()

    stream_mappings = {
        "camera-slam-left": StreamId("1201-1"),
        "camera-slam-right": StreamId("1201-2"),
        "camera-rgb": StreamId("214-1"),
        "camera-eyetracking": StreamId("211-1"),
        "imu-right": StreamId("1202-1"),
        "imu-left": StreamId("1202-2"),
        "mag": StreamId("1203-1"),
    }

    # activate the required streams

    for stream_id in stream_mappings.values():
        if stream_id in streams_in_vrs:
            deliver_option.activate_stream(stream_id)

    # set imu skip count using set_subsample_rate method if imu stream is pressent in vrs
    imu_streams = filter(
        lambda x: x in streams_in_vrs,
        [stream_mappings["imu-left"], stream_mappings["imu-right"]],
    )
    if imu_streams:
        for imu in imu_streams:
            deliver_option.set_subsample_rate(imu, args.imu_skip_count)

    # create a data iterable with chosen options
    data_stream = provider.deliver_queued_sensor_data(deliver_option)
    # iterate through data and plot
    for data in data_stream:
        device_time_ns = data.get_time_ns(TimeDomain.DEVICE_TIME)
        rr.set_time_nanos("device_time", device_time_ns)
        label = provider.get_label_from_stream_id(data.stream_id())

        if (
            data.sensor_data_type() == SensorDataType.IMAGE
            and label == _CAMERA_RGB_LABEL
        ):
            img = load_img_data(data, args.down_sampling_factor)
            rotated_img = np.rot90(img, k=1, axes=(1, 0))
            rr.log(
                _CAMERA_RGB_LABEL,
                rr.Image(rotated_img).compress(jpeg_quality=args.jpeg_quality),
            )

        elif (
            data.sensor_data_type() == SensorDataType.IMAGE
            and label == _CAMERA_ET_LABEL
        ):
            img = load_img_data(data, args.down_sampling_factor)
            rr.log(
                _CAMERA_ET_LABEL, rr.Image(img).compress(jpeg_quality=args.jpeg_quality)
            )

        elif (
            data.sensor_data_type() == SensorDataType.IMAGE
            and label == _CAMERA_SLAM_LEFT_LABEL
        ):
            img = load_img_data(data, args.down_sampling_factor)
            rotated_img = np.rot90(img, k=1, axes=(1, 0))
            rr.log(
                _CAMERA_SLAM_LEFT_LABEL,
                rr.Image(rotated_img).compress(jpeg_quality=args.jpeg_quality),
            )

        elif (
            data.sensor_data_type() == SensorDataType.IMAGE
            and label == _CAMERA_SLAM_RIGHT_LABEL
        ):
            img = load_img_data(data, args.down_sampling_factor)
            rotated_img = np.rot90(img, k=1, axes=(1, 0))
            rr.log(
                _CAMERA_SLAM_RIGHT_LABEL,
                rr.Image(rotated_img).compress(jpeg_quality=args.jpeg_quality),
            )

        elif data.sensor_data_type() == SensorDataType.IMU and label == _IMU_LEFT_LABEL:
            imu_data = data.imu_data()
            rr.log("imu-left-accl/x", rr.Scalar(imu_data.accel_msec2[0]))
            rr.log("imu-left-accl/y", rr.Scalar(imu_data.accel_msec2[1]))
            rr.log("imu-left-accl/z", rr.Scalar(imu_data.accel_msec2[2]))
            rr.log("imu-left-gyro/x", rr.Scalar(imu_data.gyro_radsec[0]))
            rr.log("imu-left-gyro/y", rr.Scalar(imu_data.gyro_radsec[1]))
            rr.log("imu-left-gyro/z", rr.Scalar(imu_data.gyro_radsec[2]))

        elif (
            data.sensor_data_type() == SensorDataType.IMU and label == _IMU_RIGHT_LABEL
        ):
            imu_data = data.imu_data()
            rr.log("imu-right-accl/x", rr.Scalar(imu_data.accel_msec2[0]))
            rr.log("imu-right-accl/y", rr.Scalar(imu_data.accel_msec2[1]))
            rr.log("imu-right-accl/z", rr.Scalar(imu_data.accel_msec2[2]))
            rr.log("imu-right-gyro/x", rr.Scalar(imu_data.gyro_radsec[0]))
            rr.log("imu-right-gyro/y", rr.Scalar(imu_data.gyro_radsec[1]))
            rr.log("imu-right-gyro/z", rr.Scalar(imu_data.gyro_radsec[2]))

        elif (
            data.sensor_data_type() == SensorDataType.MAGNETOMETER
            and label == _MAGNETOMETER_LABEL
        ):
            mag_data = data.magnetometer_data()
            rr.log("mag/x", rr.Scalar(mag_data.mag_tesla[0] * 1e6))
            rr.log("mag/y", rr.Scalar(mag_data.mag_tesla[1] * 1e6))
            rr.log("mag/z", rr.Scalar(mag_data.mag_tesla[2] * 1e6))


def main():

    logging.basicConfig(
        format="%(name)s %(asctime)-15s [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s",
        level=logging.INFO,
    )
    # load and validate args
    args = pars_args()
    check_args(args)

    # initialize rerun and set memory limit to 2GB
    rr.init("Aria Studio VRS Player")
    rr.spawn(memory_limit=args.memory_limit)

    # load the data from vrs file and plot it using rerun
    log_to_rerun(args)


if __name__ == "__main__":
    main()
