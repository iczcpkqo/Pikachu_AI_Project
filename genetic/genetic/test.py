from RubikCube import RubikCube

rubik = RubikCube()


# actions = list(rubik.faceMoveMap.keys())
for actions in rubik.PERMUTATIONS:
    cube1 = RubikCube()
    cube2 = RubikCube()
    print("action:" + str(actions))

    cube1.execute(actions)
    cube2.execute2(actions)
    print("cube1")
    print(cube1.toString(cube1.state))
    print("cube2")
    print(cube2.getFaces())
